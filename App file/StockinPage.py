import tkinter as tk
from tkinter import ttk, messagebox
import app
# Assuming this contains category and warehouse information
import Database  

class StockInPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the left side (Add Stock section)
        left_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        left_frame.pack(side=tk.LEFT, padx=(20, 10), pady=(10, 10), fill=tk.Y)

        # Title Label
        stock_label = tk.Label(left_frame, text="Add Stock to the Database", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        stock_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Input Labels and Fields with increased font size
        input_font = ("Helvetica", 14)  # Increased font size for input fields

        # Category Dropdown
        category_label = tk.Label(left_frame, text="Enter Category", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        category_label.grid(row=1, column=0, sticky="e", pady=5)
        self.category_combobox = ttk.Combobox(left_frame, values=Database.category, font=input_font)
        self.category_combobox.grid(row=1, column=1, pady=5)

        # Product Name Entry
        product_name_label = tk.Label(left_frame, text="Enter Product Name", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        product_name_label.grid(row=2, column=0, sticky="e", pady=5)
        self.product_name_entry = tk.Entry(left_frame, font=input_font)
        self.product_name_entry.grid(row=2, column=1, pady=5)

        # Description Entry
        description_label = tk.Label(left_frame, text="Enter Description", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        description_label.grid(row=3, column=0, sticky="e", pady=5)
        self.description_entry = tk.Entry(left_frame, font=input_font)
        self.description_entry.grid(row=3, column=1, pady=5)

        # Standard Cost Entry
        standard_cost_label = tk.Label(left_frame, text="Enter Standard Cost", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        standard_cost_label.grid(row=4, column=0, sticky="e", pady=5)
        self.standard_cost_entry = tk.Entry(left_frame, font=input_font)
        self.standard_cost_entry.grid(row=4, column=1, pady=5)

        # Listing Cost Entry
        listing_cost_label = tk.Label(left_frame, text="Enter Listing Cost", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        listing_cost_label.grid(row=5, column=0, sticky="e", pady=5)
        self.listing_cost_entry = tk.Entry(left_frame, font=input_font)
        self.listing_cost_entry.grid(row=5, column=1, pady=5)

        # Stocks Entry
        stocks_label = tk.Label(left_frame, text="Enter Stocks", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        stocks_label.grid(row=6, column=0, sticky="e", pady=5)
        self.stocks_entry = tk.Entry(left_frame, font=input_font)
        self.stocks_entry.grid(row=6, column=1, pady=5)

        # Warehouse Dropdown
        warehouse_label = tk.Label(left_frame, text="Select Warehouse", bg="#E6F7F7", fg="#2F4F4F", font=input_font)
        warehouse_label.grid(row=7, column=0, sticky="e", pady=5)
        self.warehouse_combobox = ttk.Combobox(left_frame, values=Database.warehouse_list(), font=input_font)
        self.warehouse_combobox.grid(row=7, column=1, pady=5)

        # Add Stock Button
        add_stock_btn = tk.Button(left_frame, text="Add Stock", command=self.add_stock, bg="#AEB8E1", fg="#2A2D34", font=input_font)
        add_stock_btn.grid(row=8, column=0, columnspan=2, pady=(20, 10))

        # Clear Fields Button
        clear_btn = tk.Button(left_frame, text="Clear All Fields", command=self.clear_fields, bg="#AEB8E1", fg="#2A2D34", font=input_font)
        clear_btn.grid(row=9, column=0, columnspan=2, pady=(0, 20))

        # Create a frame for the right side (Stock Information display)
        right_frame = tk.Frame(self, bg="#FFFFFF", bd=2, relief=tk.RAISED)
        right_frame.pack(side=tk.RIGHT, padx=(10, 20), pady=(10, 10), fill=tk.BOTH, expand=True)

        # Information Title
        info_label = tk.Label(right_frame, text="Stock Information", font=("Helvetica", 14, "bold"), bg="#FFFFFF")
        info_label.pack(pady=(10, 5))

        # Text Area for Displaying Stock Information
        self.info_text = tk.Text(right_frame, height=20, width=80, bg="#F0F0F0", fg="#2A2D34", font=("Helvetica", 12))
        self.info_text.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)  # Increased width

        # Total Label
        self.total_label = tk.Label(right_frame, text="Total Stocks: 0", font=("Helvetica", 14), bg="#FFFFFF", fg="#2F4F4F")
        self.total_label.pack(side=tk.BOTTOM, anchor='e', padx=10, pady=(10, 10))  # Align to the right bottom

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

        # Inserting product into the database
        msg = Database.insert_product(category, product_name, description, standard_cost, listing_cost, stocks, warehouse)

        # Update the text area with the new stock information
        self.info_text.insert(tk.END, f"Added Stock:\n"
                                        f"Category: {category}\n"
                                        f"Product Name: {product_name}\n"
                                        f"Description: {description}\n"
                                        f"Standard Cost: ${standard_cost:.2f}\n"
                                        f"Listing Cost: ${listing_cost:.2f}\n"
                                        f"Stocks: {stocks}\n"
                                        f"Warehouse: {warehouse}\n"
                                        f"Message: {msg}\n\n")
        app.logger.info(F"Stock In: Category: {category} Product Name: {product_name} stocked in with {stocks} in {warehouse} warehouse.\n")
        self.info_text.see(tk.END)  # Scroll to the end of the text area

        # Update the total label with the new total stocks
        self.update_total(stocks)

    def update_total(self, new_stocks):
        current_total = int(self.total_label['text'].split(': ')[1])  # Extract current total
        updated_total = current_total + new_stocks
        self.total_label['text'] = f"Total Stocks: {updated_total}"

    def clear_fields(self):
        self.category_combobox.set("")
        self.product_name_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.standard_cost_entry.delete(0, tk.END)
        self.listing_cost_entry.delete(0, tk.END)
        self.stocks_entry.delete(0, tk.END)
        self.warehouse_combobox.set("")
        self.info_text.delete(1.0, tk.END)  # Clear the text area

# Assuming Database has relevant methods for fetching warehouse and category details
