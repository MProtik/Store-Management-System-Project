import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cartpage  # Import CartPage from the cart_page module
import Product_List
from Product_List import ProductsPage  # Import ProductsPage from the previous module
import StockinPage  # Import StockInPage from the stockinpage module
from CustomerListPage import CustomerListPage
from Sold_Products_Page import SoldProductsPage
import logging
import SeeActivity

logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("log")

# Main Frame
class MainFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7FF")  # Light blue background
        center_frame.pack(pady=50, padx=(400, 0))

        total_stock_label = tk.Label(center_frame, text="Total Stock: 100", bg="#E6F7FF", fg="#2F4F4F")
        total_stock_label.pack(pady=20)

        vendor_count_label = tk.Label(center_frame, text="Vendors: 5", bg="#E6F7FF", fg="#2F4F4F")
        vendor_count_label.pack(pady=20)

        recent_activity_label = tk.Label(center_frame, text="Recent Activity: Product X added", bg="#E6F7FF", fg="#2F4F4F")
        recent_activity_label.pack(pady=20)

# New Product Page Frame
class NewProductPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7FF")  # Light blue background
        center_frame.pack(pady=50, padx=(400, 0))

        name_label = tk.Label(center_frame, text="Product Name", bg="#E6F7FF", fg="#2F4F4F")
        name_label.pack(pady=5)
        name_entry = tk.Entry(center_frame)
        name_entry.pack(pady=5)

        price_label = tk.Label(center_frame, text="Price", bg="#E6F7FF", fg="#2F4F4F")
        price_label.pack(pady=5)
        price_entry = tk.Entry(center_frame)
        price_entry.pack(pady=5)

        category_label = tk.Label(center_frame, text="Category", bg="#E6F7FF", fg="#2F4F4F")
        category_label.pack(pady=5)
        category_entry = tk.Entry(center_frame)
        category_entry.pack(pady=5)

        add_btn = tk.Button(center_frame, text="Add Product", command=lambda: messagebox.showinfo("Product", "Product Added"),
                            bg="#AEB8E1", fg="#2A2D34")
        add_btn.pack(pady=20)

# Main Application Class
class StoreManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Management System")
        self.geometry("1300x680")
        self.configure(bg="#E6F7F7")  # Light blue background

        header_frame = tk.Frame(self, bg="#B0C4DE", bd=0)  # Light gray background
        header_frame.pack(pady=0, fill='x')

        original_image = Image.open("F:/Python Code-Lab/Store-Management-System-Project/logo.png")  # Correct the path format
        logo_image = original_image.resize((80, 80), Image.LANCZOS)
        logo_image = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(header_frame, image=logo_image, bg="#B0C4DE")  # Match the frame color
        logo_label.image = logo_image
        logo_label.grid(row=0, column=0, padx=(5, 10), pady=10)

        title = tk.Label(header_frame, text="Store Management System", font=("Helvetica", 20, "bold"), fg="#2A2D34", bg="#B0C4DE")
        title.grid(row=0, column=1, sticky='w')

        # 'See Activity' Button positioned at the far right
        see_activity_btn = tk.Button(header_frame, text="See Activity", command=self.see_activity, font=("Helvetica", 10, "bold"),
                                     bg="#AEB8E1", fg="#2A2D34", width=15, height=1)
        see_activity_btn.grid(row=0, column=2, padx=(770, 20), pady=(60, 10))

        self.main_frame = MainFrame(self)
        self.new_product_page = NewProductPage(self)
        self.stock_in_page = StockinPage.StockInPage(self)  # Use the StockInPage imported from stockinpage.py
        self.cart_page = cartpage.CartPage(self)  # Use the CartPage imported from cart_page.py
        self.products_page = ProductsPage(self)  # Create instance of ProductsPage
        self.customer_list_page = CustomerListPage(self)
        self.sold_product_page = SoldProductsPage(self)  # Correct variable name
        self.activity_page = SeeActivity.LogViewerApp(self)

        sidebar_frame = tk.Frame(self, bg="#E6F7FF")  # Light blue background
        sidebar_frame.pack(side=tk.LEFT, fill='y')

        button_style = {
            "font": ("Helvetica", 10, "bold"),
            "bg": "#AEB8E1",  # Soft purple background
            "fg": "#2A2D34",  # Dark blue text
            "width": 15,
            "height": 5,
            "bd": 2,
            "relief": "solid"
        }

        # Cart button first, followed by Products button
        cart_btn = tk.Button(sidebar_frame, text="Cart", command=self.show_cart, **button_style)
        cart_btn.pack(pady=10)

        products_btn = tk.Button(sidebar_frame, text="Products", command=self.show_products, **button_style)
        products_btn.pack(pady=10)

        stock_in_btn = tk.Button(sidebar_frame, text="New Stock In", command=self.show_stock_in, **button_style)
        stock_in_btn.pack(pady=10)

        vendor_login_btn = tk.Button(sidebar_frame, text="Customers List", command=self.show_customer_list, **button_style)
        vendor_login_btn.pack(pady=10)

        new_product_btn = tk.Button(sidebar_frame, text="Sold Products", command=self.show_sold_product_page, **button_style)
        new_product_btn.pack(pady=10)

        self.content_frame = tk.Frame(self, bg="#E6F7FF")  # Light blue background
        self.content_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        # Initially show the Cart page
        self.cart_page.pack(fill='both', expand=True)
        self.main_frame.pack_forget()
        self.new_product_page.pack_forget()
        self.stock_in_page.pack_forget()
        self.products_page.pack_forget()  # Hide Products page initially
        self.customer_list_page.pack_forget()  # Hide Customers List page initially
        self.sold_product_page.pack_forget()  # Hide Sold Products page initially
        self.activity_page.pack_forget()

    def show_frame(self, frame):
        # Hide all pages, including the activity page, when switching to a new frame
        self.main_frame.pack_forget()
        self.new_product_page.pack_forget()
        self.stock_in_page.pack_forget()
        self.cart_page.pack_forget()
        self.products_page.pack_forget()  # Hide Products page when showing other frames
        self.customer_list_page.pack_forget()  # Hide Customers List page when showing other frames
        self.sold_product_page.pack_forget()  # Hide Sold Products page when showing other frames
        self.activity_page.pack_forget()  # Hide activity page when switching frames

        # Show the selected frame
        frame.pack(fill='both', expand=True)

    def show_products(self):
        self.show_frame(self.products_page)  # Show the products page

    def show_stock_in(self):
        self.show_frame(self.stock_in_page)

    def show_sold_product_page(self):
        self.show_frame(self.sold_product_page)

    def show_cart(self):
        self.show_frame(self.cart_page)

    def show_customer_list(self):
        self.show_frame(self.customer_list_page)  # Show the Customers List page

    def see_activity(self):
        # Show the activity page when "See Activity" button is pressed
        self.activity_page.pack(fill='both', expand=True)

        # Hide other pages when the activity page is shown
        self.main_frame.pack_forget()
        self.cart_page.pack_forget()
        self.new_product_page.pack_forget()
        self.stock_in_page.pack_forget()
        self.products_page.pack_forget()
        self.customer_list_page.pack_forget()
        self.sold_product_page.pack_forget()

if __name__ == "__main__":
    app = StoreManagementApp()
    app.mainloop()
