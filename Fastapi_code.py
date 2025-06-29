# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import pymysql
from sqlalchemy import create_engine

app = FastAPI()

# MySQL Connection (Update with your actual credentials)
DB_URL = "mysql+pymysql://ezyro_38900475:mokabbirai@sql203.ezyro.com/ezyro_38900475_ShopLensAi_Database"
engine = create_engine(DB_URL)

# -------------------- MODELS --------------------
class Product(BaseModel):
    category: str
    product_name: str
    description: Optional[str]
    standard_cost: float
    list_price: float
    stocks: int
    warehouse: str

class UpdateProduct(Product):
    product_id: int

class Sale(BaseModel):
    product_name: str
    quantity: int
    selling_price: float
    customer_name: Optional[str] = ""
    sold_date: str

# -------------------- UTILITY --------------------
def read_table(query: str):
    return pd.read_sql(query, engine)

# -------------------- ROUTES --------------------

@app.get("/")
def read_root():
    return {"message": "Welcome to the Store Management API"}

@app.get("/products")
def get_products():
    df = read_table("SELECT * FROM hardwarestore")
    return df.to_dict(orient="records")

@app.get("/products/{product_name}")
def get_product_by_name(product_name: str):
    df = read_table(f"SELECT * FROM hardwarestore WHERE PRODUCT_NAME = '{product_name}'")
    if df.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    return df.to_dict(orient="records")

@app.post("/products")
def insert_product(product: Product):
    df = read_table("SELECT MAX(PRODUCT_ID) AS max_id FROM hardwarestore")
    new_id = int(df["max_id"].iloc[0]) + 1 if df["max_id"].iloc[0] else 1
    query = f"""
    INSERT INTO hardwarestore
    (CATEGORY_NAME, PRODUCT_ID, PRODUCT_NAME, DESCRIPTION, STANDARD_COST, LIST_PRICE, STOCKS, WAREHOUSE_NAME)
    VALUES
    ('{product.category}', {new_id}, '{product.product_name}', '{product.description or ''}',
     {product.standard_cost}, {product.list_price}, {product.stocks}, '{product.warehouse}')
    """
    with engine.connect() as conn:
        conn.execute(query)
    return {"message": f"Product inserted with ID {new_id}"}

@app.put("/products")
def update_product(product: UpdateProduct):
    query = f"""
    UPDATE hardwarestore SET
    CATEGORY_NAME = '{product.category}',
    PRODUCT_NAME = '{product.product_name}',
    DESCRIPTION = '{product.description or ''}',
    STANDARD_COST = {product.standard_cost},
    LIST_PRICE = {product.list_price},
    STOCKS = {product.stocks},
    WAREHOUSE_NAME = '{product.warehouse}'
    WHERE PRODUCT_ID = {product.product_id}
    """
    with engine.connect() as conn:
        result = conn.execute(query)
    return {"message": f"Product {product.product_id} updated successfully"}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    with engine.connect() as conn:
        conn.execute(f"DELETE FROM hardwarestore WHERE PRODUCT_ID = {product_id}")
    return {"message": f"Product {product_id} deleted"}

@app.post("/sales")
def record_sale(sale: Sale):
    df = read_table(f"SELECT * FROM hardwarestore WHERE PRODUCT_NAME = '{sale.product_name}'")
    if df.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    product_id = df["PRODUCT_ID"].iloc[0]
    standard_cost = df["STANDARD_COST"].iloc[0]
    old_stock = df["STOCKS"].iloc[0]
    new_stock = old_stock - sale.quantity
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Not enough stock")
    total_price = sale.quantity * sale.selling_price

    with engine.connect() as conn:
        conn.execute(f"""
            INSERT INTO soldproducts
            (PRODUCT_NAME, PRODUCT_ID, QUANTITY, STANDARD_COST, SELLING_PRICE, TOTAL_PRICE, CUSTOMER_NAME, SOLD_DATE)
            VALUES
            ('{sale.product_name}', {product_id}, {sale.quantity}, {standard_cost},
             {sale.selling_price}, {total_price}, '{sale.customer_name}', '{sale.sold_date}')
        """)
        conn.execute(f"UPDATE hardwarestore SET STOCKS = {new_stock} WHERE PRODUCT_NAME = '{sale.product_name}'")

    return {"message": "Sale recorded successfully"}

@app.get("/categories")
def get_categories():
    df = read_table("SELECT DISTINCT CATEGORY_NAME FROM hardwarestore")
    return df["CATEGORY_NAME"].dropna().tolist()

@app.get("/warehouses")
def get_warehouses():
    df = read_table("SELECT DISTINCT WAREHOUSE_NAME FROM hardwarestore")
    return df["WAREHOUSE_NAME"].dropna().tolist()

@app.get("/stock/{product_name}")
def get_stock(product_name: str):
    df = read_table(f"SELECT STOCKS FROM hardwarestore WHERE PRODUCT_NAME = '{product_name}'")
    if df.empty:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"stock": int(df["STOCKS"].iloc[0])}
