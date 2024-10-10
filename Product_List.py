import tkinter as tk
from tkinter import ttk, messagebox
import Database  # Assuming your Database module contains the necessary functions
import EditPage  # Importing the EditPage module

class ProductsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Display total stock and vendor info
        total_stock_label = tk.Label(self, text=f"Total Stock: {Database.Total_stocks}")
        total_stock_label.pack(pady=10)

        vendor_count_label = tk.Label(self, text="Vendors: 5")
        vendor_count_label.pack(pady=10)

        recent_activity_label = tk.Label(self, text="Recent Activity: Product X added")
        recent_activity_label.pack(pady=10)

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

        self.show_edit_page_button = tk.Button(self, text="Show Edit Product Page", command=self.show_edit_product_page)
        self.show_edit_page_button.pack(pady=10)

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

    def open_stock_in_window(self):
        # Create a new top-level window for the Stock In functionality
        stock_in_window = tk.Toplevel(self)
        stock_in_window.title("Stock In")
        stock_in_window.geometry("400x300")

        # Select Category
        category_label = tk.Label(stock_in_window, text="Select Category:")
        category_label.pack(pady=10)
        category_combobox = ttk.Combobox(stock_in_window, values=Database.categories())
        category_combobox.pack(pady=5)

        # Select Product
        product_label = tk.Label(stock_in_window, text="Select Product:")
        product_label.pack(pady=10)
        product_combobox = ttk.Combobox(stock_in_window)
        product_combobox.pack(pady=5)

        # Function to update product list when category is selected
        def update_product_list(event):
            selected_category = category_combobox.get()
            product_combobox['values'] = Database.product_list(selected_category)

        # Bind the category combobox selection event to update product list
        category_combobox.bind("<<ComboboxSelected>>", update_product_list)

        # Show Current Stock
        current_stock_label = tk.Label(stock_in_window, text="Current Stock: 0")
        current_stock_label.pack(pady=10)

        # Update stock based on the selected product
        def update_stock_label(event):
            selected_product = product_combobox.get()
            if selected_product:
                current_stock = Database.StockAmount(selected_product)
                current_stock_label.config(text=f"Current Stock: {current_stock}")

        # Bind the product combobox selection event to update stock label
        product_combobox.bind("<<ComboboxSelected>>", update_stock_label)

        # Enter Stock Amount
        stock_amount_label = tk.Label(stock_in_window, text="Enter Stock to Add:")
        stock_amount_label.pack(pady=10)
        stock_amount_entry = tk.Entry(stock_in_window)
        stock_amount_entry.pack(pady=5)

        # Button to Add Stock
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
                
                # Update the database
                Database.StockinDatabase(total_stock, selected_product)

                # Show confirmation message
                messagebox.showinfo("Stock Updated", f"Total Stock of {selected_product} is now: {total_stock}")

                # Destroy the stock in window after updating stock
                stock_in_window.destroy()  # Close the Stock In window

            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for the stock amount.")

        add_stock_button = tk.Button(stock_in_window, text="Add Stock", command=add_stock)
        add_stock_button.pack(pady=10)

    def populate_treeview(self, data):
        # Clear the existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert new data into the treeview
        for index, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def filter_by_category(self):
        selected_category = self.category_combobox.get()
        
        # Retrieve the full product data from your DataFrame
        all_data = Database.whole_database()  # Assuming this is your DataFrame containing all products

        # Check if selected category is in the list of categories
        if selected_category in Database.categories():
            # Filter the DataFrame by the selected category
            filtered_data = all_data[all_data['CATEGORY_NAME'] == selected_category]
            # Populate the treeview with filtered data
            self.populate_treeview(filtered_data)
        else:
            messagebox.showerror("Selection Error", f"{selected_category} is not a valid category.")

    def refresh_page(self):
        # Reload the entire product data
        self.populate_treeview(Database.whole_database())
        self.category_combobox.set('')  # Clear the selected category

    def show_edit_product_page(self):
        """Function to display the EditProductPage."""
        edit_product_window = tk.Toplevel(self)  # Create a new top-level window for editing
        edit_product_window.title("Edit Product")
        edit_product_window.geometry("600x400")

        # Create an instance of the EditProductPage
        edit_page = EditPage.EditProductPage(edit_product_window)  # Pass the new window as parent
        edit_page.pack(fill='both', expand=True)

# Example of how to run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Store Management System")
    app = ProductsPage(root)  # Create instance of ProductsPage
    app.pack(expand=True, fill="both")
    root.mainloop()
