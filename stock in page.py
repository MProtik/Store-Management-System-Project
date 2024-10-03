import tkinter as tk
from tkinter import messagebox
import Dashboard

def on_enter_button(e):
    e.widget['background'] = '#5D3FD3'  # Darker purple
    e.widget['foreground'] = 'black'     # Text color black

def on_leave_button(e):
    e.widget['background'] = '#D8BFD8'  # Light purple
    e.widget['foreground'] = '#5D3FD3'  # Text color back to purple

def open_stock_in():
    stock_in_page()  # Correctly open Stock In page

def open_dashboard():
    Dashboard.dashboard_page()  # Correctly open Dashboard page

def open_vendor_login():
    messagebox.showinfo("Vendor Login", "Navigating to Vendor Login")

def open_new_product():
    new_product_page()  # Correctly open New Product page

# Dashboard Page
def dashboard_page():
    dashboard_window = tk.Toplevel()  # Create a new window
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("400x300")

    total_stock_label = tk.Label(dashboard_window, text="Total Stock: 100")
    total_stock_label.pack(pady=20)

    vendor_count_label = tk.Label(dashboard_window, text="Vendors: 5")
    vendor_count_label.pack(pady=20)

    recent_activity_label = tk.Label(dashboard_window, text="Recent Activity: Product X added")
    recent_activity_label.pack(pady=20)

# New Product Page
def new_product_page():
    new_product_window = tk.Toplevel()  # Create a new window
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

# Main Page Layout with Updated Styles
def main_page():
    root = tk.Tk()
    root.title("Store Management System")
    root.geometry("500x500")
    
    # Main page background color
    root.configure(bg="#f0f0f5")

    # Title
    title = tk.Label(root, text="Store Management System", font=("Helvetica", 24, "bold"), fg="#5D3FD3", bg="#f0f0f5", pady=20)
    title.pack()

    button_style = {
        "font": ("Helvetica", 14, "bold"),  # Using bold Helvetica for a more beautiful appearance
        "bg": "#D8BFD8",  # Light purple
        "fg": "#5D3FD3",  # Darker purple for text
        "width": 20,
        "height": 2,
        "bd": 2,
        "relief": "solid"
    }

    # Buttons for navigation with hover effect
    dashboard_btn = tk.Button(root, text="Dashboard", command=open_dashboard, **button_style)  # Added correct command
    dashboard_btn.pack(pady=10)
    dashboard_btn.bind("<Enter>", on_enter_button)
    dashboard_btn.bind("<Leave>", on_leave_button)

    stock_in_btn = tk.Button(root, text="Stock In", command=open_stock_in, **button_style)  # Added correct command
    stock_in_btn.pack(pady=10)
    stock_in_btn.bind("<Enter>", on_enter_button)
    stock_in_btn.bind("<Leave>", on_leave_button)

    vendor_login_btn = tk.Button(root, text="Vendor Login", command=open_vendor_login, **button_style)  # Vendor Login stays as is
    vendor_login_btn.pack(pady=10)
    vendor_login_btn.bind("<Enter>", on_enter_button)
    vendor_login_btn.bind("<Leave>", on_leave_button)

    new_product_btn = tk.Button(root, text="New Product", command=open_new_product, **button_style)  # Added correct command
    new_product_btn.pack(pady=10)
    new_product_btn.bind("<Enter>", on_enter_button)
    new_product_btn.bind("<Leave>", on_leave_button)

    root.mainloop()

# Stock In Page Layout
def stock_in_page():
    stock_in_window = tk.Toplevel()  # Create a new window
    stock_in_window.title("Stock In")
    stock_in_window.geometry("400x300")
    stock_in_window.configure(bg="#f0f0f5")

    # Labels and Entry fields with the new bold font
    product_label = tk.Label(stock_in_window, text="Product Name", font=("Helvetica", 12, "bold"), fg="#5D3FD3", bg="#f0f0f5")
    product_label.pack(pady=5)
    product_entry = tk.Entry(stock_in_window)
    product_entry.pack()

    quantity_label = tk.Label(stock_in_window, text="Quantity", font=("Helvetica", 12, "bold"), fg="#5D3FD3", bg="#f0f0f5")
    quantity_label.pack(pady=5)
    quantity_entry = tk.Entry(stock_in_window)
    quantity_entry.pack()

    price_label = tk.Label(stock_in_window, text="Price", font=("Helvetica", 12, "bold"), fg="#5D3FD3", bg="#f0f0f5")
    price_label.pack(pady=5)
    price_entry = tk.Entry(stock_in_window)
    price_entry.pack()

    # Submit Button
    submit_btn = tk.Button(stock_in_window, text="Submit", font=("Helvetica", 12, "bold"), bg="#D8BFD8", fg="#5D3FD3", width=15, height=1, bd=2, relief="solid")
    submit_btn.pack(pady=20)

    submit_btn.bind("<Enter>", on_enter_button)
    submit_btn.bind("<Leave>", on_leave_button)

if __name__ == "__main__":
    main_page()
