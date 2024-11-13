import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Make sure tkcalendar is installed
import Database  # Assumes Database module contains necessary functions

class CustomerListPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Frame for search, date picker, and buttons
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, fill="x")  # Fill horizontally

        # Label for search
        search_label = tk.Label(search_frame, text="Search by Name or Customer ID:")
        search_label.pack(side="left", padx=5)

        # Entry for search
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        # Search Button
        search_button = tk.Button(search_frame, text="Search", command=self.search_customer)
        search_button.pack(side="left", padx=5)

        # Date Label
        date_label = tk.Label(search_frame, text="Filter by Date:")
        date_label.pack(side="left", padx=5)

        # Date Picker (DateEntry widget)
        self.date_entry = DateEntry(search_frame, width=12, background="darkblue", foreground="white", date_pattern="yyyy-mm-dd")
        self.date_entry.pack(side="left", padx=5)

        # Date Filter Button
        date_filter_button = tk.Button(search_frame, text="Filter by Date", command=self.select_date)
        date_filter_button.pack(side="left", padx=5)

        # Refresh Button (align to the right)
        refresh_button = tk.Button(search_frame, text="Refresh", command=self.refresh_page)
        refresh_button.pack(side="right", padx=5)

        # Frame to hold the Treeview and scrollbars
        tree_frame = tk.Frame(self)
        tree_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Treeview widget for displaying customer data
        self.tree = ttk.Treeview(tree_frame, columns=list(Database.whole_customerstable().columns), show="headings")

        # Define column headings
        for col in Database.whole_customerstable().columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Vertical scrollbar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(xscrollcommand=h_scrollbar.set)
        h_scrollbar.pack(side="bottom", fill="x")

        # Pack the Treeview
        self.tree.pack(side="left", expand=True, fill="both")

        # Populate Treeview with initial customer data
        self.populate_treeview(Database.whole_customerstable())

    def populate_treeview(self, data):
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert new data
        for index, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

    def search_customer(self):
        search_value = self.search_entry.get().strip()
        if search_value:
            # Check if input is numeric (Customer ID) or not (Customer Name)
            if search_value.isdigit():  # Treat as Customer ID
                search_results = Database.SearchCustomer(int(search_value))
            else:  # Treat as Customer Name
                search_results = Database.SearchCustomer(search_value)

            if search_results.empty:
                messagebox.showinfo("Search Results", "No customer found.")
            else:
                self.populate_treeview(search_results)
        else:
            messagebox.showerror("Input Error", "Please enter a name or Customer ID to search.")

    def select_date(self):
        # Get selected date from DateEntry widget
        selected_date = self.date_entry.get()  # Format is yyyy-mm-dd
        # Filter data by date
        date_filtered_data = Database.SearchByDate(selected_date, "CustomersTable")

        if date_filtered_data.empty:
            messagebox.showinfo("Date Filter Results", "No data found for the selected date.")
        else:
            self.populate_treeview(date_filtered_data)

    def refresh_page(self):
        # Reload all customer data
        self.populate_treeview(Database.whole_customerstable())
        self.search_entry.delete(0, tk.END)  # Clear search entry

# Example of running the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Customer List Management System")
    app = CustomerListPage(root)  # Create instance of CustomerListPage
    app.pack(expand=True, fill="both")
    root.mainloop()
