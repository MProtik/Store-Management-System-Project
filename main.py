import tkinter as tk
from tkinter import ttk

class StoreManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Store management System")
        self.root.geometry("1000x600")

        # Store Data (Mock data for the example)
        self.products = {
            1: {"name": "Napkin", "price": 150},
            2: {"name": "Watch", "price": 2000},
            3: {"name": "Lollipop", "price": 20}
        }
        self.cart = []

        # Top Frame
        self.header = tk.Label(root, text="KJ Mart", font=("Arial", 30), bg="white", fg="black")
        self.header.pack(side=tk.TOP, fill=tk.X)

        # Left Frame
        self.left_frame = tk.Frame(root, width=500, height=500, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right Frame (for the cart)
        self.right_frame = tk.Frame(root, bg="orange", width=500, height=500)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Left Frame Widgets
        self.product_id_label = tk.Label(self.left_frame, text="Enter Product's ID", font=("Arial", 14), bg="white")
        self.product_id_label.pack(pady=10)
        self.product_id_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.product_id_entry.pack(pady=10)

        self.search_button = tk.Button(self.left_frame, text="Search", command=self.search_product, font=("Arial", 14))
        self.search_button.pack(pady=10)

        self.product_list_label = tk.Label(self.left_frame, text="Product List:", font=("Arial", 14), bg="white")
        self.product_list_label.pack(pady=10)

        self.product_name_label = tk.Label(self.left_frame, text="Product's Name: ", font=("Arial", 14), bg="white")
        self.product_name_label.pack(pady=10)
        
        self.product_price_label = tk.Label(self.left_frame, text="Price: Rs.", font=("Arial", 14), bg="white")
        self.product_price_label.pack(pady=10)

        self.quantity_label = tk.Label(self.left_frame, text="Enter Quantity", font=("Arial", 14), bg="white")
        self.quantity_label.pack(pady=10)
        self.quantity_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.quantity_entry.pack(pady=10)

        self.discount_label = tk.Label(self.left_frame, text="Enter Discount", font=("Arial", 14), bg="white")
        self.discount_label.pack(pady=10)
        self.discount_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.discount_entry.pack(pady=10)

        self.add_to_cart_button = tk.Button(self.left_frame, text="Add To Cart", command=self.add_to_cart, font=("Arial", 14))
        self.add_to_cart_button.pack(pady=10)

        self.given_amount_label = tk.Label(self.left_frame, text="Given Amount", font=("Arial", 14), bg="white")
        self.given_amount_label.pack(pady=10)
        self.given_amount_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.given_amount_entry.pack(pady=10)

        self.calculate_change_button = tk.Button(self.left_frame, text="Calculate Change", command=self.calculate_change, font=("Arial", 14))
        self.calculate_change_button.pack(pady=10)

        self.change_label = tk.Label(self.left_frame, text="Change: Rs. 0", font=("Arial", 14), bg="white")
        self.change_label.pack(pady=10)

        self.generate_bill_button = tk.Button(self.left_frame, text="Generate Bill", command=self.generate_bill, font=("Arial", 14), bg="red", fg="white")
        self.generate_bill_button.pack(pady=10)

        # Right Frame Widgets (for displaying the cart)
        self.cart_label = tk.Label(self.right_frame, text="Products\t\tQuantity\tAmount", font=("Arial", 16), bg="orange")
        self.cart_label.pack(pady=10)

        self.cart_list = tk.Listbox(self.right_frame, font=("Arial", 14), width=40, height=10)
        self.cart_list.pack(pady=10)

        self.total_label = tk.Label(self.right_frame, text="Total: Rs. 0", font=("Arial", 20), bg="orange")
        self.total_label.pack(pady=10)

    def search_product(self):
        product_id = int(self.product_id_entry.get())
        if product_id in self.products:
            product = self.products[product_id]
            self.product_name_label.config(text=f"Product's Name: {product['name']}")
            self.product_price_label.config(text=f"Price: Rs. {product['price']}")
        else:
            self.product_name_label.config(text="Product's Name: Not Found")
            self.product_price_label.config(text="Price: Rs. 0")

    def add_to_cart(self):
        product_id = int(self.product_id_entry.get())
        quantity = int(self.quantity_entry.get())
        discount = float(self.discount_entry.get())
        if product_id in self.products:
            product = self.products[product_id]
            discounted_price = product["price"] * (1 - discount / 100)
            total_price = discounted_price * quantity
            self.cart.append({"name": product["name"], "quantity": quantity, "price": total_price})
            self.update_cart()

    def update_cart(self):
        self.cart_list.delete(0, tk.END)
        total_amount = 0
        for item in self.cart:
            total_amount += item["price"]
            self.cart_list.insert(tk.END, f"{item['name']}\t\t{item['quantity']}\t{item['price']:.2f}")
        self.total_label.config(text=f"Total: Rs. {total_amount:.2f}")

    def calculate_change(self):
        given_amount = float(self.given_amount_entry.get())
        total_amount = float(self.total_label.cget("text").split(": Rs. ")[1])
        change = given_amount - total_amount
        self.change_label.config(text=f"Change: Rs. {change:.2f}")

    def generate_bill(self):
        print("Bill generated...")  # Replace with actual billing logic

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManagementSystem(root)
    root.mainloop()
