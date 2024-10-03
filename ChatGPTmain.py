import tkinter as tk
from tkinter import messagebox

def open_dashboard():
    messagebox.showinfo("Dashboard", "Navigating to Dashboard")

def open_stock_in():
    messagebox.showinfo("Stock In", "Navigating to Stock In Page")
    stock_in_page()

def open_vendor_login():
    messagebox.showinfo("Vendor Login", "Navigating to Vendor Login")
    vendor_login_page()

def open_new_product():
    messagebox.showinfo("New Product", "Navigating to New Product Page")
    new_product_page()



def new_product_page():
    new_product_window = tk.Toplevel()
    new_product_window.title("New Product")
    new_product_window.geometry("400x300")

    name_label = tk.Label(new_product_window, text="Product Name")
    name_label.pack()
    name_entry = tk.Entry(new_product_window)
    name_entry.pack()

    price_label = tk.Label(new_product_window, text="Price")
    price_label.pack()
    price_entry = tk.Entry(new_product_window)
    price_entry.pack()

    category_label = tk.Label(new_product_window, text="Category")
    category_label.pack()
    category_entry = tk.Entry(new_product_window)
    category_entry.pack()

    add_btn = tk.Button(new_product_window, text="Add Product", command=lambda: messagebox.showinfo("Product", "Product Added"))
    add_btn.pack(pady=20)







def main_page():
    root = tk.Tk()
    root.title("Store Management System")
    root.geometry("400x400")

    # Title
    title = tk.Label(root, text="Store Management System", font=("Arial", 20), pady=20)
    title.pack()

    # Buttons for navigation
    dashboard_btn = tk.Button(root, text="Dashboard", command=open_dashboard, width=30, pady=10)
    dashboard_btn.pack(pady=10)

    stock_in_btn = tk.Button(root, text="Stock In", command=open_stock_in, width=30, pady=10)
    stock_in_btn.pack(pady=10)

    vendor_login_btn = tk.Button(root, text="Vendor Login", command=open_vendor_login, width=30, pady=10)
    vendor_login_btn.pack(pady=10)

    new_product_btn = tk.Button(root, text="New Product", command=open_new_product, width=30, pady=10)
    new_product_btn.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_page()
