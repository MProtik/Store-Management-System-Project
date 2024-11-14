import tkinter as tk
from tkinter import ttk, messagebox
import Database
import datetime
import invoice_fillup
import app

now = datetime.datetime.now()



class CartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.selected_category = ""
        self.selected_product = ""
        self.products = []
        self.cart_items = []  # List to hold items in the cart

        self.price = 0
        self.total_amount = 0  # Initialize total amount

        # Initialize phone number variable
        self.phone_number = ""

        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        center_frame.pack(pady=10, padx=(100, 0))

        cart_label = tk.Label(center_frame, text="Shopping Cart", font=("Helvetica", 16, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        cart_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Customer Name Entry
        customer_name_label = tk.Label(center_frame, text="Customer Name", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        customer_name_label.grid(row=1, column=0, sticky="e", pady=5)
        self.customer_name_entry = tk.Entry(center_frame)
        self.customer_name_entry.grid(row=1, column=1, pady=5)

        # Phone Number Entry
        phone_number_label = tk.Label(center_frame, text="Phone Number", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        phone_number_label.grid(row=2, column=0, sticky="e", pady=5)
        self.phone_number_entry = tk.Entry(center_frame)
        self.phone_number_entry.grid(row=2, column=1, pady=5)

        # Dropdown for Category Selection
        category_label = tk.Label(center_frame, text="Select Category", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        category_label.grid(row=3, column=0, sticky="e", pady=5)
        self.category_combobox = ttk.Combobox(center_frame, values=sorted(Database.categories()))
        self.category_combobox.grid(row=3, column=1, pady=5)

        # Bind the combobox selection to an event handler
        self.category_combobox.bind("<<ComboboxSelected>>", self.store_selected_category)

        # Dropdown for Product List
        product_label = tk.Label(center_frame, text="Select Product", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        product_label.grid(row=4, column=0, sticky="e", pady=5)
        self.product_combobox = ttk.Combobox(center_frame)
        self.product_combobox.grid(row=4, column=1, pady=5)

        # Bind the product selection to get the price and stock
        self.product_combobox.bind("<<ComboboxSelected>>", self.update_price_and_stock)

        # Price Label
        self.price_label = tk.Label(center_frame, text="Price: $0", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.price_label.grid(row=5, column=0, sticky="e", pady=5)

        # Stock Label
        self.stock_label = tk.Label(center_frame, text="Stock: N/A", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.stock_label.grid(row=5, column=1, sticky="w", pady=5)

        # Quantity Entry
        quantity_label = tk.Label(center_frame, text="Enter Quantity", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        quantity_label.grid(row=6, column=0, sticky="e", pady=5)
        self.quantity_entry = tk.Entry(center_frame)
        self.quantity_entry.grid(row=6, column=1, pady=5)

        # Discount Entry
        discount_label = tk.Label(center_frame, text="Enter Discount (%)", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        discount_label.grid(row=7, column=0, sticky="e", pady=5)
        self.discount_entry = tk.Entry(center_frame)
        self.discount_entry.grid(row=7, column=1, pady=5)

        # Add to Cart Button
        add_to_cart_btn = tk.Button(center_frame, text="Add to Cart", command=self.add_to_cart, bg="#AEB8E1", fg="#2A2D34")
        add_to_cart_btn.grid(row=8, column=0, columnspan=2, pady=20)

        # Given Amount Entry
        given_amount_label = tk.Label(center_frame, text="Given Amount", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        given_amount_label.grid(row=9, column=0, sticky="e", pady=5)
        self.given_amount_entry = tk.Entry(center_frame)
        self.given_amount_entry.grid(row=9, column=1, pady=5)

        # Calculate Change Button
        calculate_change_btn = tk.Button(center_frame, text="Calculate Change", command=self.calculate_change, bg="#AEB8E1", fg="#2A2D34")
        calculate_change_btn.grid(row=10, column=0, columnspan=2, pady=10)

        # Generate Bill Button
        generate_bill_btn = tk.Button(center_frame, text="Generate Bill", command=self.generate_bill, bg="#AEB8E1", fg="#2A2D34")
        generate_bill_btn.grid(row=11, column=0, columnspan=2, pady=10)

        # Space between products and total
        tk.Label(center_frame, text="", bg="#E6F7F7").grid(row=12, column=0, columnspan=2, pady=10)  # Empty label for spacing

        # Invoice Frame - Adjusted the position slightly higher and wider
        self.invoice_frame = tk.Frame(center_frame, bg="#E6F7F7", bd=2, relief="groove", width=300)  # Increase width here
        self.invoice_frame.grid(row=0, column=2, rowspan=9, padx=70, pady=(20, 0))  # Moved it higher, adjusted padx and pady

        invoice_label = tk.Label(self.invoice_frame, text="Invoice", font=("Helvetica", 14, "bold"), fg="#2F4F4F", bg="#E6F7F7")
        invoice_label.pack(pady=10)

        # Treeview for Invoice
        self.invoice_tree = ttk.Treeview(self.invoice_frame, columns=("Product", "Quantity", "Price"), show="headings")
        self.invoice_tree.heading("Product", text="Product")
        self.invoice_tree.heading("Quantity", text="Quantity")
        self.invoice_tree.heading("Price", text="Price")
        self.invoice_tree.pack(pady=8, fill="both", expand=True)  # Allow it to expand
        self.invoice_tree.configure(height=10)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.invoice_frame, orient="vertical", command=self.invoice_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.invoice_tree.configure(yscroll=scrollbar.set)

        # Total Amount Display (Moved up and outside of the invoice frame)
        self.total_amount_label = tk.Label(center_frame, text="Total: $0.00", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12, "bold"))
        self.total_amount_label.grid(row=9, column=2, padx=70, sticky="w")

        # Given Amount and Change Display
        self.given_amount_label = tk.Label(center_frame, text="Given Amount: $0.00", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.given_amount_label.grid(row=10, column=2, padx=70, sticky="w")

        self.change_label = tk.Label(center_frame, text="Change: $0.00", bg="#E6F7F7", fg="#2F4F4F", font=("Helvetica", 12))
        self.change_label.grid(row=11, column=2, padx=70, sticky="w")

    def store_selected_category(self, event):
        self.selected_category = self.category_combobox.get()
        self.products = sorted(Database.product_list(self.selected_category))
        self.product_combobox['values'] = self.products
        self.product_combobox.set("")  # Clear the selected product

    def update_price_and_stock(self, event):
        self.selected_product = self.product_combobox.get()
        self.price = Database.product_price(self.selected_product)
        self.price_label.config(text=f"Price: ${self.price}")
        stock_amount = Database.StockAmount(self.selected_product)
        if stock_amount == 0:
            self.stock_label.config(text="Out of Stock", fg="red")
        else:
            self.stock_label.config(text=f"Stock: {stock_amount}", fg="#2F4F4F")

    def add_to_cart(self):
        quantity = int(self.quantity_entry.get() or 1)
        discount = float(self.discount_entry.get() or 0)

        if quantity > Database.StockAmount(self.selected_product):
            messagebox.showerror("Insufficient Stock", "Not enough stock available.")
            return

        # Calculate the price after discount
        final_price = self.price * quantity * (1 - discount / 100)

        # Add item to cart
        self.cart_items.append((self.selected_product, quantity, final_price))
        self.total_amount += final_price  # Update the total amount

        # Update total amount label
        self.total_amount_label.config(text=f"Total: ${self.total_amount:.2f}")

        # Update Invoice Treeview
        self.invoice_tree.insert("", "end", values=(self.selected_product, quantity, f"${final_price:.2f}"))

        # Clear category and product selections and input fields
        self.category_combobox.set("")  # Clear selected category
        self.product_combobox.set("")    # Clear selected product
        self.quantity_entry.delete(0, tk.END)  # Clear quantity field
        self.discount_entry.delete(0, tk.END)   # Clear discount field


    def calculate_change(self):
        try:
            given_amount = float(self.given_amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid given amount.")
            return

        if given_amount < self.total_amount:
            messagebox.showerror("Insufficient Amount", "Given amount is less than the total amount.")
            return

        change = given_amount - self.total_amount
        self.change_label.config(text=f"Change: ${change:.2f}")
        self.given_amount_label.config(text=f"Given Amount: ${given_amount:.2f}")

    def generate_bill(self):

        # Code to generate a bill could go here (e.g., saving to a file or printing)
        #date
        sold_date = now.strftime('%Y-%m-%d %H:%M')
        bill_content = f"Date: {now.strftime('%Y-%m-%d %H:%M')}\n"
        #name
        name = self.customer_name_entry.get() or ""
        bill_content += f"Customer Name: {name}\n"
        #phone number
        phone_number = self.phone_number_entry.get() or ""
        bill_content += f"Phone Number: {phone_number}\n\n"
        total = self.total_amount
        #Products
        l = []
        bill_content += "Products:\n"

        data = {
            "[Name]": name,
            "[Phone]": str(phone_number),
            '[total]': str(total),
            '[date]':str(sold_date),
            '[invoice id]': '',
        }

        i = 1
        for product, quantity, price in self.cart_items:
            bill_content += f"{product} - Quantity: {quantity}, Price: ${price:.2f}\n"
            l.append(product)
            Database.product_sold(product, quantity)
            Database.insert_soldproduct(product, quantity, price, name, sold_date)
            data[f"[Product{i}]"] = product
            data[f"[amount{i}]"] = str(quantity)
            data[f"[price{i}]"] = str(price)
            i += 1
            
        products = ', '.join(l)

        bill_content += f"\nTotal Amount: ${total:.2f}\n"
        bill_content += self.given_amount_label.cget("text") + "\n"  # Get the label text for given amount
        bill_content += self.change_label.cget("text") + "\n"  # Get the label text for change

        
        Database.insert_customerstable(name, phone_number, products, total, bill_content, sold_date)
        print(name, phone_number, products, total, bill_content, sold_date)
        
 
        invoice_fillup.fill_invoice(data)

        app.logger.info(f"Purchase: {name} purchased {products}. Bill = {total}\n")       
        self.reset_cart()

    def reset_cart(self):
        self.cart_items.clear()
        self.total_amount = 0
        self.total_amount_label.config(text="Total: $0.00")
        self.invoice_tree.delete(*self.invoice_tree.get_children())
        self.customer_name_entry.delete(0, tk.END)
        self.phone_number_entry.delete(0, tk.END)
        self.given_amount_entry.delete(0, tk.END)
        self.change_label.config(text="Change: $0.00")
        self.given_amount_label.config(text="Given Amount: $0.00")
        self.quantity_entry.delete(0, tk.END)
        self.discount_entry.delete(0, tk.END)

