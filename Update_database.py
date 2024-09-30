import tkinter as tk
from tkinter import messagebox

class UpdateDatabase:
    def __init__(self, root):
        self.root = root
        self.root.title("Update the database")
        self.root.geometry("800x400")

        # Header
        self.header = tk.Label(root, text="Update the database", font=("Arial", 30), bg="white", fg="blue")
        self.header.pack(side=tk.TOP, fill=tk.X)

        # Left Frame for form inputs
        self.left_frame = tk.Frame(root, width=500, height=500, bg="white")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Right Frame for ID information
        self.right_frame = tk.Frame(root, bg="lightgrey", width=300, height=500)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Left Frame Widgets
        self.id_label = tk.Label(self.left_frame, text="Enter Id", font=("Arial", 14), bg="white")
        self.id_label.pack(pady=5)
        self.id_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.id_entry.pack(pady=5)

        self.product_name_label = tk.Label(self.left_frame, text="Enter Product Name", font=("Arial", 14), bg="white")
        self.product_name_label.pack(pady=5)
        self.product_name_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.product_name_entry.pack(pady=5)

        self.stocks_label = tk.Label(self.left_frame, text="Enter Stocks", font=("Arial", 14), bg="white")
        self.stocks_label.pack(pady=5)
        self.stocks_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.stocks_entry.pack(pady=5)

        self.cost_price_label = tk.Label(self.left_frame, text="Enter Cost Price", font=("Arial", 14), bg="white")
        self.cost_price_label.pack(pady=5)
        self.cost_price_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.cost_price_entry.pack(pady=5)

        self.selling_price_label = tk.Label(self.left_frame, text="Enter Selling Price", font=("Arial", 14), bg="white")
        self.selling_price_label.pack(pady=5)
        self.selling_price_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.selling_price_entry.pack(pady=5)

        self.total_cost_price_label = tk.Label(self.left_frame, text="Enter Total Cost Price", font=("Arial", 14), bg="white")
        self.total_cost_price_label.pack(pady=5)
        self.total_cost_price_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.total_cost_price_entry.pack(pady=5)

        self.total_selling_price_label = tk.Label(self.left_frame, text="Enter Total Selling Price", font=("Arial", 14), bg="white")
        self.total_selling_price_label.pack(pady=5)
        self.total_selling_price_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.total_selling_price_entry.pack(pady=5)

        self.vendor_name_label = tk.Label(self.left_frame, text="Enter Vendor Name", font=("Arial", 14), bg="white")
        self.vendor_name_label.pack(pady=5)
        self.vendor_name_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.vendor_name_entry.pack(pady=5)

        self.vendor_phone_label = tk.Label(self.left_frame, text="Enter Vendor Phone Number", font=("Arial", 14), bg="white")
        self.vendor_phone_label.pack(pady=5)
        self.vendor_phone_entry = tk.Entry(self.left_frame, font=("Arial", 14))
        self.vendor_phone_entry.pack(pady=5)

        self.update_button = tk.Button(self.left_frame, text="Update Database", command=self.update_database, font=("Arial", 14), bg="blue", fg="white")
        self.update_button.pack(pady=10)

        # Right Frame Widgets (for ID info)
        self.id_info_label = tk.Label(self.right_frame, text="ID has reached upto: 0", font=("Arial", 14), bg="lightgrey")
        self.id_info_label.pack(pady=100)

    def update_database(self):
        # Simulating a database update with a message
        messagebox.showinfo("Success", "Update database Successful")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpdateDatabase(root)
    root.mainloop()
