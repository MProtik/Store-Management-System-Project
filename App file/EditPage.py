import tkinter as tk
from tkinter import messagebox
import Database  # Assuming your Database module contains the necessary functions
import app

class EditProductPage(tk.Toplevel):
    def __init__(self, parent, product_id):
        super().__init__(parent)
        self.parent = parent
        self.product_id = product_id
        self.title("Edit Product")
        self.geometry("800x400")

        # Prevent multiple edit windows from opening
        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        # Retrieve product details from the database using SearchByProductID
        product_details = Database.SearchByProductID(self.product_id)

        # Debug: Print column names to verify
        print("Actual DataFrame columns:", product_details.columns)

        # Define labels and corresponding keys based on expected DataFrame column names
        labels = [
            ("Category Name", "CATEGORY_NAME"),
            ("Product Name", "PRODUCT_NAME"),
            ("Description", "DESCRIPTION"),
            ("Standard Cost", "STANDARD_COST"),
            ("Listing Cost", "LIST_PRICE"),
            ("Stocks", "STOCKS"),
            ("Warehouse Name", "WAREHOUSE_NAME")
        ]
        self.entries = {}

        # Create entry fields with pre-filled values
        for label_text, data_key in labels:
            frame = tk.Frame(self)
            frame.pack(pady=5)

            label_widget = tk.Label(frame, text=label_text)
            label_widget.pack(side="left")

            entry = tk.Entry(frame)
            entry.pack(side="left")
            self.entries[data_key] = entry

            # Insert value into entry if it exists in the DataFrame
            if data_key in product_details.columns:
                entry.insert(0, product_details[data_key].iloc[0])
            else:
                print(f"Key '{data_key}' not found in DataFrame columns.")

        # Save button
        save_button = tk.Button(self, text="Save Changes", command=self.save_changes)
        save_button.pack(pady=10)

    def save_changes(self):
        # Collect updated data from entries
        updated_data = {key: entry.get() for key, entry in self.entries.items()}
        print(updated_data)

        # Unpack the values from the dictionary and update the database
        category = updated_data.get('CATEGORY_NAME')
        product_name = updated_data.get('PRODUCT_NAME')
        description = updated_data.get('DESCRIPTION')
        standard_cost = updated_data.get('STANDARD_COST')
        listing_cost = updated_data.get('LIST_PRICE')
        stocks = updated_data.get('STOCKS')
        warehouse_name = updated_data.get('WAREHOUSE_NAME')

        # Update the database with the unpacked values
        Database.update_product(self.product_id, category, product_name, description, standard_cost, listing_cost, stocks, warehouse_name)
        app.logger.warning(f"Edited: Product Name = {Database.SearchByProductID(self.product_id)["PRODUCT_NAME"].iloc[0]} Product ID = {self.product_id} has been Edited in the software.\n")

        messagebox.showinfo("Success", "Product details updated successfully.")
        self.destroy()  # Close the edit window

# Assuming that the necessary database functions like `SearchByProductID` and `update_product` exist in the Database module.
