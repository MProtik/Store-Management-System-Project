import tkinter as tk
from tkinter import ttk, messagebox
import Database  # Assuming this contains category and warehouse information

class StockInPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        center_frame.pack(pady=10, padx=(100, 0))

        # Title Label
        stock_label = tk.Label(center_frame, text="Add Stock to the Database", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        stock_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Category Dropdown
        category_label = tk.Label(center_frame, text="Enter Category", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        category_label.grid(row=1, column=0, sticky="e", pady=5)
        self.category_combobox = ttk.Combobox(center_frame, values=Database.category)
        self.category_combobox.grid(row=1, column=1, pady=5)

        # Product Name Entry
        product_name_label = tk.Label(center_frame, text="Enter Product Name", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        product_name_label.grid(row=2, column=0, sticky="e", pady=5)
        self.product_name_entry = tk.Entry(center_frame)
        self.product_name_entry.grid(row=2, column=1, pady=5)

        # Description Entry
        description_label = tk.Label(center_frame, text="Enter Description", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        description_label.grid(row=3, column=0, sticky="e", pady=5)
        self.description_entry = tk.Entry(center_frame)
        self.description_entry.grid(row=3, column=1, pady=5)

        # Standard Cost Entry
        standard_cost_label = tk.Label(center_frame, text="Enter Standard Cost", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        standard_cost_label.grid(row=4, column=0, sticky="e", pady=5)
        self.standard_cost_entry = tk.Entry(center_frame)
        self.standard_cost_entry.grid(row=4, column=1, pady=5)

        # Listing Cost Entry
        listing_cost_label = tk.Label(center_frame, text="Enter Listing Cost", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        listing_cost_label.grid(row=5, column=0, sticky="e", pady=5)
        self.listing_cost_entry = tk.Entry(center_frame)
        self.listing_cost_entry.grid(row=5, column=1, pady=5)

        # Stocks Entry
        stocks_label = tk.Label(center_frame, text="Enter Stocks", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        stocks_label.grid(row=6, column=0, sticky="e", pady=5)
        self.stocks_entry = tk.Entry(center_frame)
        self.stocks_entry.grid(row=6, column=1, pady=5)

        # Warehouse Dropdown
        warehouse_label = tk.Label(center_frame, text="Select Warehouse", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        warehouse_label.grid(row=7, column=0, sticky="e", pady=5)
        self.warehouse_combobox = ttk.Combobox(center_frame, values=Database.warehouse_list())
        self.warehouse_combobox.grid(row=7, column=1, pady=5)

        # Add Stock Button
        add_stock_btn = tk.Button(center_frame, text="Add Stock", command=self.add_stock, bg="#AEB8E1", fg="#2A2D34")
        add_stock_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Clear Fields Button
        clear_btn = tk.Button(center_frame, text="Clear All Fields", command=self.clear_fields, bg="#AEB8E1", fg="#2A2D34")
        clear_btn.grid(row=9, column=0, columnspan=2, pady=10)

    def add_stock(self):
        # Extract and validate input data
        category = self.category_combobox.get()
        product_name = self.product_name_entry.get()
        description = self.description_entry.get()

        try:
            standard_cost = float(self.standard_cost_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Standard Cost.")
            return

        try:
            listing_cost = float(self.listing_cost_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid Listing Cost.")
            return

        try:
            stocks = int(self.stocks_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of Stocks.")
            return

        warehouse = self.warehouse_combobox.get()

        #def update_product(category, product_name, description, standard_cost, list_price, stocks, warehouse):
        msg = Database.update_product(category, product_name, description, standard_cost, listing_cost, stocks, warehouse)

        messagebox.showinfo("Success", msg)

    def clear_fields(self):
        self.category_combobox.set("")
        self.product_name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.standard_cost_entry.delete(0, tk.END)
        self.listing_cost_entry.delete(0, tk.END)
        self.stocks_entry.delete(0, tk.END)
        self.warehouse_combobox.set("")

# Assuming Database has relevant methods for fetching warehouse and category details
