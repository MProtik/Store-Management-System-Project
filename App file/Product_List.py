import tkinter as tk
from tkinter import messagebox, ttk
import Database  # Assuming you have a Database module for managing data
import EditPage
import logging

logging.basicConfig(level = logging.INFO, filename = "app.log", filemode = "a",
                    format = "%(asctime)s - %(levelname)s - %(message)s" 
)
logger = logging.getLogger("log")

class ProductsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Display total stock dynamically
        total_stock_label = tk.Label(self, text=f"Total Stock: {Database.totalstocks()}")
        total_stock_label.pack(pady=10)
        
        # Create a frame to hold the filter frame and stock in button
        top_frame = tk.Frame(self)
        top_frame.pack(fill="x", padx=10, pady=5)

        # Create a frame for filtering and stock in button
        filter_stock_frame = tk.Frame(top_frame)
        filter_stock_frame.pack(side="left", anchor="nw", padx=5, pady=5)

        # Create a label for the category filter
        filter_label = tk.Label(filter_stock_frame, text="Filter by Category:")
        filter_label.pack(side="left", padx=5)

        # Create a Combobox for category selection
        self.category_combobox = ttk.Combobox(filter_stock_frame, values=Database.categories())
        self.category_combobox.pack(side="left", padx=5)

        # Create a button to apply the filter
        filter_button = tk.Button(filter_stock_frame, text="Filter", command=self.filter_by_category)
        filter_button.pack(side="left", padx=5)

        # Stock In Button
        stock_in_button = tk.Button(filter_stock_frame, text="Stock In", command=self.open_stock_in_window)
        stock_in_button.pack(side="left", padx=5)

        # Search Product Section
        search_frame = tk.Frame(top_frame)
        search_frame.pack(side="left", anchor="nw", padx=5, pady=5)

        # Create a label for search box
        search_label = tk.Label(search_frame, text="Search Product:")
        search_label.pack(side="left", padx=5)

        # Create an entry widget for search input
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        # Create a button to trigger search
        search_button = tk.Button(search_frame, text="Search", command=self.search_product)
        search_button.pack(side="left", padx=5)

        # Create a frame to hold the refresh button on the right
        refresh_frame = tk.Frame(top_frame)
        refresh_frame.pack(side="right", anchor="ne", padx=5, pady=5)

        # Refresh Button
        refresh_button = tk.Button(refresh_frame, text="Refresh", command=self.refresh_page)
        refresh_button.pack()

        # Create a frame to hold the Treeview and scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a Treeview widget to display the DataFrame
        self.tree = ttk.Treeview(tree_frame, columns=list(Database.whole_database().columns), show="headings")
        self.tree.bind("<Button-3>", self.show_context_menu)  # Right-click context menu binding

        # Define headings
        for col in Database.whole_database().columns:
            self.tree.heading(col, text=col)  # Set the column heading
            self.tree.column(col, anchor="center")  # Center the column text

        # Insert DataFrame rows into the Treeview
        self.populate_treeview(Database.whole_database())

        # Create a vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

        # Create a horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        # Pack the Treeview
        self.tree.pack(side="left", expand=True, fill="both")

        # Context menu for right-click options
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Edit", command=self.edit_selected)
        self.context_menu.add_command(label="Delete", command=self.delete_selected)

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)

        if item not in self.tree.selection():
            self.tree.selection_set(item)

        selected_items = self.tree.selection()

        if len(selected_items) == 1:
            self.context_menu.entryconfig("Edit", state="normal")
            self.context_menu.entryconfig("Delete", state="normal")
        else:
            self.context_menu.entryconfig("Edit", state="disabled")
            self.context_menu.entryconfig("Delete", state="normal")

        self.context_menu.post(event.x_root, event.y_root)

    def edit_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select an item to edit.")
            return

        item = selected_items[0]
        product_id = self.tree.item(item, 'values')[1]
        print(f"Edit product with ID: {product_id}")

        try:
            edit_window = EditPage.EditProductPage(self, product_id)
            edit_window.grab_set()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the edit window: {str(e)}")

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select items to delete.")
            return

        if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected items?"):
            for item in selected_items:
                product_id = self.tree.item(item, 'values')[1]
                print(f"Deleting product with ID: {product_id}")
                logger.warning(f"Deleted: Product Name = {Database.SearchByProductID(product_id)["PRODUCT_NAME"].iloc[0]} Product ID = {product_id} has been deleted from the software.\n")
                Database.delete_product(product_id)
                self.tree.delete(item)

            messagebox.showinfo("Deletion", "Selected items deleted successfully.")

    def open_stock_in_window(self):
        stock_in_window = tk.Toplevel(self)
        stock_in_window.title("Stock In")
        stock_in_window.geometry("400x300")

        category_label = tk.Label(stock_in_window, text="Select Category:")
        category_label.pack(pady=10)
        category_combobox = ttk.Combobox(stock_in_window, values=Database.categories())
        category_combobox.pack(pady=5)

        product_label = tk.Label(stock_in_window, text="Select Product:")
        product_label.pack(pady=10)
        product_combobox = ttk.Combobox(stock_in_window)
        product_combobox.pack(pady=5)

        def update_product_list(event):
            selected_category = category_combobox.get()
            product_combobox['values'] = Database.product_list(selected_category)

        category_combobox.bind("<<ComboboxSelected>>", update_product_list)

        current_stock_label = tk.Label(stock_in_window, text="Current Stock: 0")
        current_stock_label.pack(pady=10)

        def update_stock_label(event):
            selected_product = product_combobox.get()
            if selected_product:
                current_stock = Database.StockAmount(selected_product)
                current_stock_label.config(text=f"Current Stock: {current_stock}")

        product_combobox.bind("<<ComboboxSelected>>", update_stock_label)

        stock_amount_label = tk.Label(stock_in_window, text="Enter Stock to Add:")
        stock_amount_label.pack(pady=10)
        stock_amount_entry = tk.Entry(stock_in_window)
        stock_amount_entry.pack(pady=5)

        def add_stock():
            selected_product = product_combobox.get()
            if not selected_product:
                messagebox.showerror("Selection Error", "Please select a product.")
                return

            try:
                stock_to_add = int(stock_amount_entry.get())
                if stock_to_add < 0:
                    raise ValueError("Stock amount cannot be negative.")

                current_stock = Database.StockAmount(selected_product)
                total_stock = current_stock + stock_to_add
                
                Database.StockinDatabase(total_stock, selected_product)
                
                logger.warning(f"A stock of {stock_to_add} is added to the Product Name = {selected_product} Product ID = {Database.SearchByProductName(selected_product)["PRODUCT_ID"].iloc[0]}.\n")

                messagebox.showinfo("Stock Updated", f"Total Stock of {selected_product} is now: {total_stock}")

                stock_in_window.destroy()

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the stock amount.")

        add_stock_button = tk.Button(stock_in_window, text="Add Stock", command=add_stock)
        add_stock_button.pack(pady=20)

    def filter_by_category(self):
        selected_category = self.category_combobox.get()
        if selected_category:
            filtered_products = Database.filter_by_category(selected_category)
            self.populate_treeview(filtered_products)
        else:
            messagebox.showwarning("Selection Error", "Please select a category to filter.")

    def refresh_page(self):
        self.populate_treeview(Database.whole_database())

    def search_product(self):
        search_value = self.search_entry.get().strip()
        if search_value:
            if search_value.isdigit():  # Product ID is expected to be an integer
                search_results = Database.SearchProductInDatabase(int(search_value))
            else:
                search_results = Database.SearchProductInDatabase(search_value)

            if search_results.empty:
                messagebox.showinfo("Search Results", "No product found.")
            else:
                self.populate_treeview(search_results)
        else:
            messagebox.showerror("Input Error", "Please enter a name or Product ID to search.")

    def populate_treeview(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for index, row in data.iterrows():
            self.tree.insert("", "end", values=row.tolist())


# Example main application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Store Management System")
    app = ProductsPage(root)
    app.pack(expand=True, fill="both")
    root.mainloop()
