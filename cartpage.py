import tkinter as tk
from tkinter import ttk, messagebox
import Database

class CartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_category = ""
        self.selected_product = ""
        self.products = []
        self.create_widgets()
        self.price = 0

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        center_frame.pack(pady=10, padx=(100, 0))

        cart_label = tk.Label(center_frame, text="Shopping Cart", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        cart_label.pack(pady=20)

        # Dropdown for Category Selection
        category_label = tk.Label(center_frame, text="Select Category", bg="#E6F7F7", fg="#2F4F4F")
        category_label.pack(pady=5)
        self.category_combobox = ttk.Combobox(center_frame, values=Database.category)
        self.category_combobox.pack(pady=5)

        # Bind the combobox selection to an event handler
        self.category_combobox.bind("<<ComboboxSelected>>", self.store_selected_category)

        # Dropdown for Product List
        product_label = tk.Label(center_frame, text="Select Product", bg="#E6F7F7", fg="#2F4F4F")
        product_label.pack(pady=5)
        
        # Initialize product_combobox without any values initially
        self.product_combobox = ttk.Combobox(center_frame)
        self.product_combobox.pack(pady=5)

        # Bind the product selection to get the price
        self.product_combobox.bind("<<ComboboxSelected>>", self.product_price)

        # Price Label
        self.price_label = tk.Label(center_frame, text="Price: $0", bg="#E6F7F7", fg="#2F4F4F")
        self.price_label.pack(pady=5)

        # Quantity Entry
        quantity_label = tk.Label(center_frame, text="Enter Quantity", bg="#E6F7F7", fg="#2F4F4F")
        quantity_label.pack(pady=5)
        self.quantity_entry = tk.Entry(center_frame)
        self.quantity_entry.pack(pady=5)

        # Discount Entry
        discount_label = tk.Label(center_frame, text="Enter Discount (%)", bg="#E6F7F7", fg="#2F4F4F")
        discount_label.pack(pady=5)
        self.discount_entry = tk.Entry(center_frame)
        self.discount_entry.pack(pady=5)

        # Add to Cart Button
        add_to_cart_btn = tk.Button(center_frame, text="Add to Cart", command=self.add_to_cart, bg="#AEB8E1", fg="#2A2D34")
        add_to_cart_btn.pack(pady=20)

        # Given Amount Entry
        given_amount_label = tk.Label(center_frame, text="Given Amount", bg="#E6F7F7", fg="#2F4F4F")
        given_amount_label.pack(pady=5)
        self.given_amount_entry = tk.Entry(center_frame)
        self.given_amount_entry.pack(pady=5)

        # Calculate Change Button
        calculate_change_btn = tk.Button(center_frame, text="Calculate Change", command=self.calculate_change, bg="#AEB8E1", fg="#2A2D34")
        calculate_change_btn.pack(pady=10)

        # Generate Bill Button
        generate_bill_btn = tk.Button(center_frame, text="Generate Bill", command=self.generate_bill, bg="#AEB8E1", fg="#2A2D34")
        generate_bill_btn.pack(pady=10)

    def store_selected_category(self, event):
        # Store the selected category and update products
        self.selected_category = self.category_combobox.get()
        self.products = Database.product_list(self.selected_category)
        
        # Update the product_combobox with the retrieved products
        self.product_combobox['values'] = self.products
        self.product_combobox.set("")  # Clear the selected product
        self.price_label.config(text="Price: $0")  # Reset price label

    def product_price(self, event):
        # Get the selected product
        self.selected_product = self.product_combobox.get()
        
        # Fetch the price using Database.product_price()
        self.price = Database.product_price(self.selected_product)
        
        # Update the price label
        self.price_label.config(text=f"Price: ${self.price:.2f}")

    def add_to_cart(self):
        product = self.product_combobox.get()
        quantity = int(self.quantity_entry.get())
        discount = float(self.discount_entry.get())
        price = Database.product_price(product)  # Get the price using Database
        discounted_price = price - (price * (discount / 100))
        self.price = discounted_price * quantity
        messagebox.showinfo("Cart", f"{product} added to cart. Total: ${self.price:.2f}")

    def calculate_change(self):
        total_amount = float(self.given_amount_entry.get())  # Replace this with the actual total bill amount
        change = total_amount - self.price  # Replace 500 with the actual total bill amount
        messagebox.showinfo("Change", f"Change: ${change:.2f}")

    def generate_bill(self):
        messagebox.showinfo("Bill", "Bill generated. Thank you for shopping!")

# Example usage (assuming Database module and its methods are defined)
if __name__ == "__main__":
    root = tk.Tk()
    app = CartPage(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
