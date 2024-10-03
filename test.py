import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Dashboard Page Frame
class DashboardPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        total_stock_label = tk.Label(self, text="Total Stock: 100")
        total_stock_label.pack(pady=20)

        vendor_count_label = tk.Label(self, text="Vendors: 5")
        vendor_count_label.pack(pady=20)

        recent_activity_label = tk.Label(self, text="Recent Activity: Product X added")
        recent_activity_label.pack(pady=20)

# New Product Page Frame
class NewProductPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        name_label = tk.Label(self, text="Product Name")
        name_label.pack()
        name_entry = tk.Entry(self)
        name_entry.pack()

        price_label = tk.Label(self, text="Price")
        price_label.pack()
        price_entry = tk.Entry(self)
        price_entry.pack()

        category_label = tk.Label(self, text="Category")
        category_label.pack()
        category_entry = tk.Entry(self)
        category_entry.pack()

        add_btn = tk.Button(self, text="Add Product", command=lambda: messagebox.showinfo("Product", "Product Added"))
        add_btn.pack(pady=20)

# Stock In Page Frame
class StockInPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        product_label = tk.Label(self, text="Product Name", font=("Helvetica", 12, "bold"), fg="#5D3FD3")
        product_label.pack(pady=5)
        product_entry = tk.Entry(self)
        product_entry.pack()

        quantity_label = tk.Label(self, text="Quantity", font=("Helvetica", 12, "bold"), fg="#5D3FD3")
        quantity_label.pack(pady=5)
        quantity_entry = tk.Entry(self)
        quantity_entry.pack()

        price_label = tk.Label(self, text="Price", font=("Helvetica", 12, "bold"), fg="#5D3FD3")
        price_label.pack(pady=5)
        price_entry = tk.Entry(self)
        price_entry.pack()

        submit_btn = tk.Button(self, text="Submit", font=("Helvetica", 12, "bold"), bg="#D8BFD8", fg="#5D3FD3", width=15, height=1, bd=2, relief="solid")
        submit_btn.pack(pady=20)

# Main Application Class
class StoreManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Management System")
        self.geometry("800x700")
        self.configure(bg="#f0f0f5")

        # Create a frame for the title and logo with a light gray background and no border
        header_frame = tk.Frame(self, bg="#d3d3d3", bd=0)  # No border
        header_frame.pack(pady=0, fill='x')  # Set pady to 0 for no space at the top

        # Load and resize the logo
        original_image = Image.open("F:/Python Code-Lab/Store-Management-System-Project/logo.png")  # Correct the path format
        logo_image = original_image.resize((80, 80), Image.LANCZOS)  # Resize to 80x80 pixels
        logo_image = ImageTk.PhotoImage(logo_image)  # Convert to PhotoImage for Tkinter

        # Logo Label
        logo_label = tk.Label(header_frame, image=logo_image, bg="#d3d3d3")  # Match the frame color
        logo_label.image = logo_image  # Keep a reference to avoid garbage collection
        logo_label.grid(row=0, column=0, padx=(5, 10), pady=10)  # Align the logo to the left with padding

        # Title Label
        title = tk.Label(header_frame, text="Store Management System", font=("Helvetica", 20, "bold"), fg="#5D3FD3", bg="#d3d3d3")  # Match the frame color
        title.grid(row=0, column=1, sticky='w')  # Align the title next to the logo

        # Create frames for different pages
        self.dashboard_page = DashboardPage(self)
        self.new_product_page = NewProductPage(self)
        self.stock_in_page = StockInPage(self)

        # Create a frame for sidebar buttons
        sidebar_frame = tk.Frame(self, bg="#f0f0f5")
        sidebar_frame.pack(side=tk.LEFT, fill='y')

        button_style = {
            "font": ("Helvetica", 10, "bold"),
            "bg": "#D8BFD8",
            "fg": "#5D3FD3",
            "width": 15,
            "height": 5,
            "bd": 2,
            "relief": "solid"
        }

        # Buttons for navigation
        dashboard_btn = tk.Button(sidebar_frame, text="Dashboard", command=self.show_dashboard, **button_style)
        dashboard_btn.pack(pady=10)

        stock_in_btn = tk.Button(sidebar_frame, text="Stock In", command=self.show_stock_in, **button_style)
        stock_in_btn.pack(pady=10)

        vendor_login_btn = tk.Button(sidebar_frame, text="Vendor Login", command=self.show_vendor_login, **button_style)
        vendor_login_btn.pack(pady=10)

        new_product_btn = tk.Button(sidebar_frame, text="New Product", command=self.show_new_product, **button_style)
        new_product_btn.pack(pady=10)

        # Create a main content area to display the selected pages
        self.content_frame = tk.Frame(self, bg="#f0f0f5")
        self.content_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        # Show the dashboard page by default
        self.dashboard_page.pack(fill='both', expand=True)

    def show_frame(self, frame):
        # Hide all frames
        self.dashboard_page.pack_forget()
        self.new_product_page.pack_forget()
        self.stock_in_page.pack_forget()

        # Show the requested frame
        frame.pack(fill='both', expand=True)

    def show_dashboard(self):
        self.show_frame(self.dashboard_page)

    def show_stock_in(self):
        self.show_frame(self.stock_in_page)

    def show_new_product(self):
        self.show_frame(self.new_product_page)

    def show_vendor_login(self):
        messagebox.showinfo("Vendor Login", "Navigating to Vendor Login")

if __name__ == "__main__":
    app = StoreManagementApp()
    app.mainloop()
