import tkinter as tk
from tkinter import ttk, messagebox
import Database

class CartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.search_results = []  # Variable to store search results
        self.selected_category = ""
        self.products = []
        self.create_widgets()

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

        # Search Button
        search_btn = tk.Button(center_frame, text="Search", command=self.store_selected_category, bg="#AEB8E1", fg="#2A2D34")
        search_btn.pack(pady=10)

        # Dropdown for Product List
        product_label = tk.Label(center_frame, text="Select Product", bg="#E6F7F7", fg="#2F4F4F")
        product_label.pack(pady=5)
        
        # Initialize product_combobox without any values initially
        self.product_combobox = ttk.Combobox(center_frame)
        self.product_combobox.pack(pady=5)

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

    def store_selected_category(self):
        # Store the selected category and update products
        self.selected_category = self.category_combobox.get()
        self.products = Database.product_list(self.selected_category)
        
        # Update the product_combobox with the retrieved products
        self.product_combobox['values'] = self.products
        self.product_combobox.set("")  # Clear the selected product

    def add_to_cart(self):
        product = self.product_combobox.get()
        quantity = int(self.quantity_entry.get())
        discount = float(self.discount_entry.get())
        price = self.get_price(product)
        discounted_price = price - (price * (discount / 100))
        total_price = discounted_price * quantity
        messagebox.showinfo("Cart", f"{product} added to cart. Total: ${total_price:.2f}")

    def get_price(self, product):
        # Simulate price fetching (replace with actual price fetching logic)
        prices = {
            "Laptop": 1000, "Phone": 500, "Tablet": 300,
            "Rice": 20, "Flour": 15, "Oil": 10,
            "Shirt": 30, "Jeans": 40, "Jacket": 60,
            "Watch": 100, "Belt": 20, "Sunglasses": 50
        }
        return prices.get(product, 0)

    def calculate_change(self):
        total_amount = float(self.given_amount_entry.get())  # Replace this with the actual total bill amount
        change = total_amount - 500  # Replace 500 with the actual total bill amount
        messagebox.showinfo("Change", f"Change: ${change:.2f}")

    def generate_bill(self):
        messagebox.showinfo("Bill", "Bill generated. Thank you for shopping!")

# Example usage (assuming Database module and its methods are defined)
if __name__ == "__main__":
    root = tk.Tk()
    app = CartPage(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
