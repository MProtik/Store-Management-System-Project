import tkinter as tk
from tkinter import ttk

class ShoppingCartPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg="#E6F7F7")  # Light blue background
        center_frame.pack(pady=10, padx=(100, 0))

        # Dropdown for Category Selection
        category_label = tk.Label(center_frame, text="Select Category", bg="#E6F7F7", fg="#2F4F4F")
        category_label.pack(pady=5)
        
        # Create a Combobox for category selection
        self.category_combobox = ttk.Combobox(center_frame, values=["Fruits", "Vegetables", "Dairy"])
        self.category_combobox.pack(pady=5)

        # Button to confirm selection
        select_btn = tk.Button(center_frame, text="Select", command=self.print_selected_category)
        select_btn.pack(pady=10)

    def print_selected_category(self):
        # Retrieve the selected category and print it
        selected_category = self.category_combobox.get()
        print(f"Selected Category: {selected_category}")

# Example usage in the main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingCartPage(root)
    app.pack()
    root.mainloop()
