import tkinter as tk
from tkinter import ttk
import pandas as pd
import Database  # Assuming your Database module contains Dataset.df

class ProductsPage(tk.Frame):  # Changed class name from DashboardPage to ProductsPage
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
        for index, row in Database.df.iterrows():
            self.tree.insert("", "end", values=list(row))

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

# Example usage in your main application
class StoreManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Store Management System")
        self.geometry("1100x670")

        # Create an instance of the ProductsPage and pack it
        self.products_page = ProductsPage(self)  # Changed instance name to products_page
        self.products_page.pack(fill='both', expand=True)

# Main Loop
if __name__ == "__main__":
    app = StoreManagementApp()
    app.mainloop()
