import tkinter as tk
from tkinter import ttk, messagebox
import Database

class CartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_category = ""
        self.selected_product = ""
        self.products = []
        self.cart_items = []  # List to hold items in the cart

        self.price = 0
        self.total_amount = 0  # Initialize total amount
        self.total_item = None  # To track the total row in the treeview

        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        center_frame.pack(pady=10, padx=(100, 0))

        cart_label = tk.Label(center_frame, text="Shopping Cart", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        cart_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Dropdown for Category Selection
        category_label = tk.Label(center_frame, text="Select Category", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        category_label.grid(row=1, column=0, sticky="e", pady=5)
        self.category_combobox = ttk.Combobox(center_frame, values=Database.category)
        self.category_combobox.grid(row=1, column=1, pady=5)

        # Bind the combobox selection to an event handler
        self.category_combobox.bind("<<ComboboxSelected>>", self.store_selected_category)

        # Dropdown for Product List
        product_label = tk.Label(center_frame, text="Select Product", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        product_label.grid(row=2, column=0, sticky="e", pady=5)
        self.product_combobox = ttk.Combobox(center_frame)
        self.product_combobox.grid(row=2, column=1, pady=5)

        # Bind the product selection to get the price
        self.product_combobox.bind("<<ComboboxSelected>>", self.product_price)

        # Price Label
        self.price_label = tk.Label(center_frame, text="Price: $0", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.price_label.grid(row=3, column=0, sticky="e", pady=5)

        # Quantity Entry
        quantity_label = tk.Label(center_frame, text="Enter Quantity", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        quantity_label.grid(row=4, column=0, sticky="e", pady=5)
        self.quantity_entry = tk.Entry(center_frame)
        self.quantity_entry.grid(row=4, column=1, pady=5)

        # Discount Entry
        discount_label = tk.Label(center_frame, text="Enter Discount (%)", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        discount_label.grid(row=5, column=0, sticky="e", pady=5)
        self.discount_entry = tk.Entry(center_frame)
        self.discount_entry.grid(row=5, column=1, pady=5)

        # Add to Cart Button
        add_to_cart_btn = tk.Button(center_frame, text="Add to Cart", command=self.add_to_cart, bg="#AEB8E1", fg="#2A2D34")
        add_to_cart_btn.grid(row=6, column=0, columnspan=2, pady=20)

        # Given Amount Entry
        given_amount_label = tk.Label(center_frame, text="Given Amount", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        given_amount_label.grid(row=7, column=0, sticky="e", pady=5)
        self.given_amount_entry = tk.Entry(center_frame)
        self.given_amount_entry.grid(row=7, column=1, pady=5)

        # Calculate Change Button
        calculate_change_btn = tk.Button(center_frame, text="Calculate Change", command=self.calculate_change, bg="#AEB8E1", fg="#2A2D34")
        calculate_change_btn.grid(row=8, column=0, columnspan=2, pady=10)

        # Generate Bill Button
        generate_bill_btn = tk.Button(center_frame, text="Generate Bill", command=self.generate_bill, bg="#AEB8E1", fg="#2A2D34")
        generate_bill_btn.grid(row=9, column=0, columnspan=2, pady=10)

        # Space between products and total
        tk.Label(center_frame, text="", bg="#E6F7F7").grid(row=10, column=0, columnspan=2, pady=10)  # Empty label for spacing

        # Invoice Frame
        self.invoice_frame = tk.Frame(center_frame, bg="#E6F7F7", bd=2, relief="groove")
        self.invoice_frame.grid(row=0, column=2, rowspan=10, padx=20, pady=20)

        invoice_label = tk.Label(self.invoice_frame, text="Invoice", font=("Helvetica", 14, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        invoice_label.pack(pady=10)

        # Treeview for Invoice
        self.invoice_tree = ttk.Treeview(self.invoice_frame, columns=("Product", "Quantity", "Price"), show="headings")
        self.invoice_tree.heading("Product", text="Product")
        self.invoice_tree.heading("Quantity", text="Quantity")
        self.invoice_tree.heading("Price", text="Price")
        self.invoice_tree.pack(pady=10)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.invoice_frame, orient="vertical", command=self.invoice_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.invoice_tree.configure(yscroll=scrollbar.set)

        # Add the total row at the bottom of the invoice
        self.add_total_row()

        # Given Amount and Change Display
        self.given_amount_label = tk.Label(self.invoice_frame, text="Given Amount: $0.00", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.given_amount_label.pack(pady=5)

        self.change_label = tk.Label(self.invoice_frame, text="Change: $0.00", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.change_label.pack(pady=5)

    def add_total_row(self):
        """This method adds a total row in the invoice TreeView."""
        self.total_item = self.invoice_tree.insert("", "end", values=("Total", "", f"${self.total_amount:.2f}"), tags=('total',))

    def store_selected_category(self, event):
        self.selected_category = self.category_combobox.get()
        self.products = Database.product_list(self.selected_category)
        self.product_combobox['values'] = self.products
        self.product_combobox.set("")  # Clear the selected product
        self.price_label.config(text="Price: $0")  # Reset price label

    def product_price(self, event):
        self.selected_product = self.product_combobox.get()
        self.price = Database.product_price(self.selected_product)
        self.price_label.config(text=f"Price: ${self.price:.2f}")

    def add_to_cart(self):
        product = self.product_combobox.get()
        try: 
            quantity = int(self.quantity_entry.get())
        except ValueError:
            quantity = 1

        try:
            discount = float(self.discount_entry.get())
        except ValueError:
            discount = 0
        
        price = Database.product_price(product)  # Get the price using Database
        discounted_price = price - (price * (discount / 100))
        total_price = discounted_price * quantity
        self.cart_items.append((product, quantity, total_price))

        # Insert product details in the invoice TreeView above the total row
        self.invoice_tree.insert("", self.invoice_tree.index(self.total_item), values=(product, quantity, f"${total_price:.2f}"))

        # Update total amount
        self.total_amount += total_price
        self.update_total_row()

        messagebox.showinfo("Cart", f"{product} added to cart. Total: ${total_price:.2f}")

    def update_total_row(self):
        """This method updates the total amount row in the TreeView."""
        self.invoice_tree.item(self.total_item, values=("Total", "", f"${self.total_amount:.2f}"))

    def calculate_change(self):
        try:
            given_amount = float(self.given_amount_entry.get())
            total_bill = sum(item[2] for item in self.cart_items)  # Calculate total bill
            change = given_amount - total_bill

            # Update given amount and change labels
            self.given_amount_label.config(text=f"Given Amount: ${given_amount:.2f}")
            self.change_label.config(text=f"Change: ${change:.2f}" if change >= 0 else "Change: Not Enough")

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def generate_bill(self):
        if not self.cart_items:
            messagebox.showwarning("Empty Cart", "Add items to the cart before generating a bill.")
            return

        # Logic to generate bill can be added here

        messagebox.showinfo("Bill Generated", "Bill has been generated successfully.")

# Assuming Database is already defined elsewhere in your application
