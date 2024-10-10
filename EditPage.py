import tkinter as tk
from tkinter import ttk, messagebox
import Database  # Assuming this contains category and warehouse information

class EditProductPage(tk.Frame):
    def __init__(self, parent, item_value=None):
        super().__init__(parent)
        parent.geometry("600x600")  # Setting the window size to 600x700
        parent.title("Edit Product Details")
        self.create_widgets()

    def create_widgets(self):
        # Creating a central frame for the UI elements with light blue background
        center_frame = tk.Frame(self, bg="#E6F7F7")
        center_frame.pack(pady=10, padx=(100, 0))

        # Title Label
        edit_label = tk.Label(center_frame, text="Edit Product Details", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        edit_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Label and Entry for Product ID
        id_label = tk.Label(center_frame, text="Enter Product ID:", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        id_label.grid(row=1, column=0, sticky="e", pady=5)

        self.id_entry = tk.Entry(center_frame)
        self.id_entry.grid(row=1, column=1, pady=5)

        # Search Button
        search_button = tk.Button(center_frame, text="Search", command=self.search_product, bg="#AEB8E1", fg="#2A2D34")
        search_button.grid(row=1, column=2, padx=5)

        # Category Dropdown
        category_label = tk.Label(center_frame, text="Enter Category", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        category_label.grid(row=2, column=0, sticky="e", pady=5)
        self.category_combobox = ttk.Combobox(center_frame, values=Database.category)
        self.category_combobox.grid(row=2, column=1, pady=5)

        # Product Name Entry
        product_name_label = tk.Label(center_frame, text="Enter Product Name", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        product_name_label.grid(row=3, column=0, sticky="e", pady=5)
        self.product_name_entry = tk.Entry(center_frame)
        self.product_name_entry.grid(row=3, column=1, pady=5)

        # Description Entry
        description_label = tk.Label(center_frame, text="Enter Description", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        description_label.grid(row=4, column=0, sticky="e", pady=5)
        self.description_entry = tk.Entry(center_frame)
        self.description_entry.grid(row=4, column=1, pady=5)

        # Standard Cost Entry
        standard_cost_label = tk.Label(center_frame, text="Enter Standard Cost", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        standard_cost_label.grid(row=5, column=0, sticky="e", pady=5)
        self.standard_cost_entry = tk.Entry(center_frame)
        self.standard_cost_entry.grid(row=5, column=1, pady=5)

        # Listing Cost Entry
        listing_cost_label = tk.Label(center_frame, text="Enter Listing Cost", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        listing_cost_label.grid(row=6, column=0, sticky="e", pady=5)
        self.listing_cost_entry = tk.Entry(center_frame)
        self.listing_cost_entry.grid(row=6, column=1, pady=5)

        # Stocks Entry
        stocks_label = tk.Label(center_frame, text="Enter Stocks", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        stocks_label.grid(row=7, column=0, sticky="e", pady=5)
        self.stocks_entry = tk.Entry(center_frame)
        self.stocks_entry.grid(row=7, column=1, pady=5)

        # Warehouse Dropdown using Database.warehouselist()
        warehouse_label = tk.Label(center_frame, text="Select Warehouse", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        warehouse_label.grid(row=8, column=0, sticky="e", pady=5)
        self.warehouse_combobox = ttk.Combobox(center_frame, values=Database.warehouse_list())
        self.warehouse_combobox.grid(row=8, column=1, pady=5)

        # Save Changes Button
        save_button = tk.Button(center_frame, text="Save Changes", command=self.save_changes, bg="#AEB8E1", fg="#2A2D34")
        save_button.grid(row=9, column=0, columnspan=3, pady=20)

        # Clear Fields Button
        clear_button = tk.Button(center_frame, text="Clear All Fields", command=self.clear_fields, bg="#AEB8E1", fg="#2A2D34")
        clear_button.grid(row=10, column=0, columnspan=3, pady=10)

    def search_product(self):
        product_id = self.id_entry.get()
        if not product_id:
            messagebox.showerror("Input Error", "Please enter a Product ID.")
            return

        product_data = Database.FilteredByProductID(product_id)
        
        if isinstance(product_data, str):  # Check if it's an error message
            messagebox.showerror("Not Found", product_data)
            self.clear_fields()
            return
        
        # Assuming product_data is a DataFrame with one row
        row = product_data.iloc[0]  # Get the first (and should be the only) row

        # Populate fields with product information
        self.category_combobox.set(row['CATEGORY_NAME'])
        self.product_name_entry.delete(0, tk.END)
        self.product_name_entry.insert(0, row['PRODUCT_NAME'])

        self.description_entry.delete(0, tk.END)
        self.description_entry.insert(0, row['DESCRIPTION'])

        self.standard_cost_entry.delete(0, tk.END)
        self.standard_cost_entry.insert(0, row['STANDARD_COST'])

        self.listing_cost_entry.delete(0, tk.END)
        self.listing_cost_entry.insert(0, row['LIST_PRICE'])

        self.stocks_entry.delete(0, tk.END)
        self.stocks_entry.insert(0, row['STOCKS'])

        self.warehouse_combobox.set(row['WAREHOUSE_NAME'])

    def save_changes(self):
        product_id = self.id_entry.get()
        if not product_id:
            messagebox.showerror("Input Error", "Please enter a Product ID.")
            return

        # Get updated values
        category = self.category_combobox.get()
        product_name = self.product_name_entry.get()
        description = self.description_entry.get()
        standard_cost = self.standard_cost_entry.get()
        listing_cost = self.listing_cost_entry.get()
        stocks = self.stocks_entry.get()
        warehouse = self.warehouse_combobox.get()

        try:
            # Convert numeric values
            standard_cost = float(standard_cost)
            listing_cost = float(listing_cost)
            stocks = int(stocks)

            # Call the function to update the product in the database
            Database.update_product(product_id, category, product_name, description, standard_cost, listing_cost, stocks, warehouse)

            messagebox.showinfo("Success", "Product details updated successfully.")

            # Refresh the entire database
            Database.whole_database()  # This will refresh the database to pull the updated data

            self.clear_fields()  # Clear fields after saving
            
            self.destroy()  # Destroy the page after saving

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid values for cost and stock.")

    def clear_fields(self):
        self.id_entry.delete(0, tk.END)
        self.category_combobox.set("")
        self.product_name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.standard_cost_entry.delete(0, tk.END)
        self.listing_cost_entry.delete(0, tk.END)
        self.stocks_entry.delete(0, tk.END)
        self.warehouse_combobox.set("")
