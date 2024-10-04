import pandas as pd
import sqlite3
import cartpage

conn = sqlite3.connect('database.db', timeout=10)  # Example with a timeout
conn.execute("PRAGMA busy_timeout = 3000")  # 3 seconds

df = pd.read_sql_query("select * from hardwarestore", conn)

category = list(set(df["CATEGORY_NAME"]))

query = pd.read_sql_query(f"select PRODUCT_NAME from hardwarestore where CATEGORY_NAME = '{category[2]}';", conn) 

def product_list(category):
    return list(set(df[df["CATEGORY_NAME"] == category]["PRODUCT_NAME"]))

def product_price(product):
    return float(df[df["PRODUCT_NAME"] == product]["LIST_PRICE"])

Total_stocks = df["STOCKS"].sum()

conn.close()


if __name__ == "__main__":
    print(category)
    print(product_price('Asus Z10PE-D8 WS'))

