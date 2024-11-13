import pandas as pd
import sqlite3

conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
conn.execute("PRAGMA busy_timeout = 3000")  # 3 seconds

df = pd.read_sql_query("select * from hardwarestore", conn)
warehouse_id = pd.read_sql_query("select WAREHOUSE_NAME, WAREHOUSE_ID from hardwarestore;", conn).drop_duplicates()
category = list(set(df["CATEGORY_NAME"]))

query = pd.read_sql_query(f"select PRODUCT_NAME from hardwarestore where CATEGORY_NAME = '{category[2]}';", conn) 

def product_list(category):
    df = whole_database()
    return list(set(df[df["CATEGORY_NAME"] == category]["PRODUCT_NAME"]))

def product_price(product):
    df = whole_database()
    return float(df[df["PRODUCT_NAME"] == product]["LIST_PRICE"].iloc[0])

def warehouse_list():
    df = whole_database()
    return list(set(df["WAREHOUSE_NAME"]))

def StockAmount(name):
    df = whole_database()
    num = int(df[df["PRODUCT_NAME"] == name]["STOCKS"].iloc[0])
    return num

def whole_database():
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    database = pd.read_sql_query("select * from hardwarestore ORDER BY PRODUCT_NAME ASC", conn)
    conn.close()
    return database

def whole_customerstable():
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    database = pd.read_sql_query("select * from customerstable;", conn)
    conn.close()
    return database

def whole_soldproduct_table():
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    database = pd.read_sql_query("select * from soldproducts;", conn)
    conn.close()
    return database

def totalstocks():
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    database = pd.read_sql_query("select * from hardwarestore;", conn)
    conn.close()
    return database["STOCKS"].sum()

def delete_product(ID):
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hardwarestore WHERE PRODUCT_ID = ?", ((ID,)))
    conn.commit()
    conn.close()

def SearchProduct(entity):
    table = whole_soldproduct_table()
    if isinstance(entity, int):
        return table[table["PRODUCT_ID"] == entity]
    elif isinstance(entity, str):
        return table[table["PRODUCT_NAME"].str.contains(entity, case=False, na=False)]
    return pd.DataFrame()

def SearchProductInDatabase(entity):
    table = whole_database()
    if isinstance(entity, int):
        return table[table["PRODUCT_ID"] == entity]
    elif isinstance(entity, str):
        return table[table["PRODUCT_NAME"].str.contains(entity, case=False, na=False)]
    return pd.DataFrame()

def SearchByDate(date, table):
    conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()
    if table == "CustomersTable":
        df = pd.read_sql_query(f"select * from {table} where Sold_Date like '{date}%'", conn) 
    elif table == "soldproducts":
        df = pd.read_sql_query(f"select * from {table} where SOLD_DATE like '{date}%'", conn) 
    else:
        print("Table name doesn't match")
    conn.close()
    return df


def SearchByProductID(ID):   #tThis was FilteredByProductID(ID)
    df = whole_database()
    result = df[df["PRODUCT_ID"] == int(ID)]
    if len(result) != 0:
        return result
    elif len(result) == 0:
        return f'There is no Product with {ID} ID'

def SearchByProductName(name):
    df = whole_database()
    result = df[df["PRODUCT_NAME"] == name]
    if len(result) != 0:
        return result
    elif len(result) == 0:
        return f'There is no Product with name = {name}'


def filter_by_category(category):
    df = whole_database()
    df = df[df["CATEGORY_NAME"] == category]
    return df


def StockinDatabase(total_stock, value) -> None:
    try:
        conn = sqlite3.connect('storedatabase.db', timeout=10)  # Example with a timeout
        conn.execute("PRAGMA busy_timeout = 3000")
        cursor = conn.cursor()
        if value.isdigit():
            conn.execute(f"UPDATE hardwarestore SET STOCKS = {total_stock} WHERE PRODUCT_ID = {value}")
        else:
            conn.execute(f"UPDATE hardwarestore SET STOCKS = {total_stock} WHERE PRODUCT_NAME = '{value}'")
        conn.commit()
    except sqlite3.Error as e:
        # Handle any error here
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

Total_stocks = whole_database()["STOCKS"].sum()



def warehouselist():
    data = pd.read_sql_query("select WAREHOUSE_NAME from hardwarestore;", conn).drop_duplicates()

    return list(data)

def categories():
    data = whole_database()["CATEGORY_NAME"]
    # data = pd.read_sql_query("select CATEGORY_NAME from hardwarestore;", conn).drop_duplicates()
    return sorted(list(data.drop_duplicates()))



#Database.update_product(product_id, category, product_name, description, standard_cost, listing_cost, stocks, warehouse)

import time

def insert_product(category, product_name, description, standard_cost, list_price, stocks, warehouse):
    conn = None
    try:
        # Connect to the SQLite database with a timeout
        conn = sqlite3.connect('storedatabase.db', timeout=10)
        conn.execute("PRAGMA busy_timeout = 3000")
        cursor = conn.cursor()

        # SQL Insert query with placeholders
        insert_query = '''
            INSERT INTO hardwarestore (CATEGORY_NAME, PRODUCT_ID, PRODUCT_NAME, DESCRIPTION, STANDARD_COST, LIST_PRICE, STOCKS, WAREHOUSE_NAME)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''

        # Handle optional description
        description = description if description else ""

        # Generate a new product ID
        product_id = len(whole_database()) + 1

        # Try inserting the product until successful
        while True:
            try:
                cursor.execute(insert_query, (category, product_id, product_name, description, standard_cost, list_price, stocks, warehouse))
                conn.commit()
                break
            except sqlite3.IntegrityError:
                # Increment product ID if conflict occurs
                product_id += 1

        return f"Product with ID: {product_id} inserted successfully."

    except sqlite3.Error as e:
        return f"Error occurred: {e}"

    finally:
        # Close the database connection
        if conn:
            conn.close()

def insert_customerstable(customer_name, phone_number, Product_list, Total, Invoice, Sold_date):
    conn = None
    try:
        # Connect to the SQLite database with a timeout
        conn = sqlite3.connect('storedatabase.db', timeout=10)
        conn.execute("PRAGMA busy_timeout = 3000")
        cursor = conn.cursor()

        # SQL Insert query with placeholders
        insert_query = '''
            INSERT INTO customerstable (CustomerID, customer_name, phone_number, Product_list, Total, Invoice, Sold_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        # Handle optional customer name and phone number
        customer_name = customer_name if customer_name else ""
        phone_number = phone_number if phone_number else ""
        
        # Calculate CustomerID based on the existing customer records
        Customer_id = len(whole_customerstable())

        while True:
            try:
                # Execute the insert query
                cursor.execute(insert_query, (Customer_id, customer_name, phone_number, Product_list, Total, Invoice, Sold_date))
                conn.commit()
                return f"Customer with ID: {Customer_id} inserted successfully."
            except sqlite3.IntegrityError:
                # Increment CustomerID if there's a conflict (e.g., duplicate)
                Customer_id += 1

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()



def get_all_customers():
    return whole_customerstable()["CustomerID"]

import sqlite3

def product_sold(product_name, qty):
    stocks = whole_database()
    num = int(stocks[stocks["PRODUCT_NAME"] == product_name]['STOCKS'].iloc[0])
    
    if num == 0:
        return 0
    else:
        conn = sqlite3.connect('storedatabase.db')
        cursor = conn.cursor()

        new_stock = num - qty

        cursor.execute("UPDATE hardwarestore SET STOCKS = ? WHERE PRODUCT_NAME = ?", (new_stock, product_name))
        
        conn.commit()

        conn.close()

        return num

def update_product(product_id, category, product_name, description, standard_cost, listing_cost, stocks, warehouse):

    conn = sqlite3.connect('storedatabase.db', timeout = 10)
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()

    UPDATE_QUERY = """
    UPDATE hardwarestore SET
    CATEGORY_NAME = ?,
    PRODUCT_NAME = ?,
    DESCRIPTION = ?,
    STANDARD_COST = ?,
    LIST_PRICE = ?,
    STOCKS = ?,
    WAREHOUSE_NAME = ? WHERE PRODUCT_ID = ?
    """
    cursor.execute(UPDATE_QUERY, (category, product_name, description, standard_cost, listing_cost, stocks, warehouse, product_id))
    conn.commit()

    conn.close()
    print(f"Product with ID: {product_id} inserted successfully.")

def SearchCustomer(entity):
    # Check if the entity is an integer (for CustomerID search)
    customer_table = whole_customerstable()
    if isinstance(entity, int):
        return customer_table[customer_table["CustomerID"] == entity]
    # Check if the entity is a string (for Customer_Name search)
    elif isinstance(entity, str):
        return customer_table[customer_table["Customer_Name"].str.lower() == entity.lower()]



def insert_soldproduct(PRODUCT_NAME, QUANTITY, SELLING_PRICE, CUSTOMER_NAME, SOLD_DATE):
    df = whole_database()
    conn = sqlite3.connect('storedatabase.db', timeout = 10)
    conn.execute("PRAGMA busy_timeout = 3000")
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO soldproducts
    (PRODUCT_NAME, PRODUCT_ID, QUANTITY, STANDARD_COST, SELLING_PRICE, TOTAL_PRICE, CUSTOMER_NAME, SOLD_DATE)
    VALUES
    (?,?,?,?,?,?,?,?)
    """

    CUSTOMER_NAME = CUSTOMER_NAME if CUSTOMER_NAME else ""
    PRODUCT_ID = df[df["PRODUCT_NAME"] == PRODUCT_NAME]["PRODUCT_ID"].iloc[0]
    STANDARD_COST = df[df["PRODUCT_NAME"] == PRODUCT_NAME]["STANDARD_COST"].iloc[0]
    TOTAL_PRICE = QUANTITY * SELLING_PRICE



    cursor.execute(insert_query, (PRODUCT_NAME, int(PRODUCT_ID), QUANTITY, float(STANDARD_COST), SELLING_PRICE, TOTAL_PRICE, CUSTOMER_NAME, SOLD_DATE))
    conn.commit()

    conn.close()
    


conn.close()


# if __name__ == "__main__":
#     print(categories())
#     print(product_price('Asus Z10PE-D8 WS'))
#     print(SearchedByProductID(2168970))
#     print(StockAmount('Asus Z10PE-D8 WS'))
    

