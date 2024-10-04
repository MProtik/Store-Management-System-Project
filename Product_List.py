import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import Database  # Assuming your Database module contains Dataset.df

class ProductsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        total_stock_label = tk.Label(self, text=f"Total Stock: {Database.Total_stocks}")
        total_stock_label.pack(pady=10)

        vendor_count_label = tk.Label(self, text="Vendors: 5")
        vendor_count_label.pack(pady=10)

        recent_activity_label = tk.Label(self, text="Recent Activity: Product X added")
        recent_activity_label.pack(pady=10)

        # Create a frame to hold the Treeview and scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a Treeview widget to display the DataFrame
        self.tree = ttk.Treeview(tree_frame, columns=list(Database.df.columns), show="headings")

        # Define headings
        for col in Database.df.columns:
            self.tree.heading(col, text=col)  # Set the column heading
            self.tree.column(col, anchor="center")  # Center the column text

        # Insert DataFrame rows into the Treeview
        self.populate_treeview(Database.df)

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

        # Create a frame for filtering
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=10)

        # Create a label for the category filter
        filter_label = tk.Label(filter_frame, text="Filter by Category:")
        filter_label.pack(side="left", padx=5)

        # Create a Combobox for category selection
        self.category_combobox = ttk.Combobox(filter_frame, values=Database.category)
        self.category_combobox.pack(side="left", padx=5)

        # Create a button to apply the filter
        filter_button = tk.Button(filter_frame, text="Filter", command=self.filter_by_category)
        filter_button.pack(side="left", padx=5)

    def populate_treeview(self, df):
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert rows into the Treeview
        for index, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def filter_by_category(self):
        selected_category = self.category_combobox.get()
        
        
        # Clear the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Filter DataFrame by the selected category
        filtered_df = Database.df[Database.df['CATEGORY_NAME'] == selected_category]

        # Debugging output

        # Insert filtered rows into the Treeview
        for index, row in filtered_df.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Check if no results found


# Example usage in your main application
class StoreManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Management System")
        self.geometry("1100x670")

        # Create an instance of the ProductsPage and pack it
        self.products_page = ProductsPage(self)
        self.products_page.pack(fill='both', expand=True)

# Main Loop
if __name__ == "__main__":
    app = StoreManagementApp()
    app.mainloop()
