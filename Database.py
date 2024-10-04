import pandas as pd
import sqlite3
import cartpage

conn = sqlite3.connect("storedatabase.db")

df = pd.read_sql_query("select * from hardwarestore", conn)

category = list(set(df["CATEGORY_NAME"]))

query = pd.read_sql_query(f"select PRODUCT_NAME from hardwarestore where CATEGORY_NAME = '{category[2]}';", conn) 

def product_list(category):
    return list(set(df[df["CATEGORY_NAME"] == category]["PRODUCT_NAME"]))
products = dict(df[["CATEGORY_NAME", "PRODUCT_NAME"]])


if __name__ == "__main__":
    print(category)
    print(products)

