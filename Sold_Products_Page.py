import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import Database  # Ensure your Database module is imported correctly
from datetime import datetime

class SoldProductsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the search entry and buttons
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, fill="x")  # Fill horizontally

        # Label for search
        search_label = tk.Label(search_frame, text="Search by Name or Product ID:")
        search_label.pack(side="left", padx=5)

        # Entry for search
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        # Search Button
        search_button = tk.Button(search_frame, text="Search", command=self.search_product)
        search_button.pack(side="left", padx=5)

        # Refresh Button (pack to the right)
        refresh_button = tk.Button(search_frame, text="Refresh", command=self.refresh_page)
        refresh_button.pack(side="right", padx=5)

        # Label for date selection
        date_label = tk.Label(search_frame, text="Select Date:")
        date_label.pack(side="left", padx=5)

        # Add DateEntry widget for selecting date
        self.date_entry = DateEntry(search_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(side="left", padx=5)

        # Filter by Date Button
        filter_date_button = tk.Button(search_frame, text="Filter by Date", command=self.filter_by_date)
        filter_date_button.pack(side="left", padx=5)

        # Create a frame to hold the Treeview and scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a Treeview widget to display the sold products DataFrame
        self.tree = ttk.Treeview(tree_frame, columns=list(Database.whole_soldproduct_table().columns), show="headings")

        # Define headings
        for col in Database.whole_soldproduct_table().columns:
            self.tree.heading(col, text=col)  # Set the column heading
            self.tree.column(col, anchor="center")  # Center the column text

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

        # Create a label to display the total selling price
        self.total_selling_label = tk.Label(self, text="Total Sold = 0.00", font=("Helvetica", 12, "bold"))
        self.total_selling_label.pack(pady=10)  # Pack it to the bottom of the frame

        # Populate the Treeview with initial sold products data
        self.populate_treeview(Database.whole_soldproduct_table())

    def populate_treeview(self, data):
        # Clear the existing data in the treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert new data into the treeview
        for index, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

        # Update the total selling price
        self.update_total_selling(data)

    def update_total_selling(self, data):
        # Calculate the total selling price from the TOTAL_PRICE column
        total_selling = self.totalsold(data)
        self.total_selling_label.config(text=f"Total Sold = {total_selling:.2f}")

    def totalsold(self, df):
        return df["TOTAL_PRICE"].sum() if "TOTAL_PRICE" in df.columns else 0

    def search_product(self):
        search_value = self.search_entry.get().strip()
        if search_value:
            # Check if the input is numeric (Product ID) or not (Product Name)
            if search_value.isdigit():  # Product ID is expected to be an integer
                search_results = Database.SearchProduct(int(search_value))
            else:  # Otherwise treat it as a Product Name
                search_results = Database.SearchProduct(search_value)

            if search_results.empty:
                messagebox.showinfo("Search Results", "No product found.")
                self.total_selling_label.config(text="Total Sold = 0.00")  # Reset total when no product found
            else:
                # Populate the treeview with search results
                self.populate_treeview(search_results)
        else:
            messagebox.showerror("Input Error", "Please enter a name or Product ID to search.")

    def filter_by_date(self):
        selected_date = self.date_entry.get_date()  # Get the selected date from DateEntry
        search_results = Database.SearchByDate(selected_date, "soldproducts")
        if search_results.empty:
            messagebox.showinfo("Filter Results", "No products found for the selected date.")
            self.total_selling_label.config(text="Total Sold = 0.00")  # Reset total when no products found
        else:
            # Populate the treeview with filtered results
            self.populate_treeview(search_results)

    def refresh_page(self):
        # Reload the entire sold products data
        self.populate_treeview(Database.whole_soldproduct_table())
        self.search_entry.delete(0, tk.END)  # Clear the search entry
        self.date_entry.set_date(datetime.now().date())  # Reset date to today

# Example of how to run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sold Products Management System")
    app = SoldProductsPage(root)  # Create instance of SoldProductsPage
    app.pack(expand=True, fill="both")
    root.mainloop()
