import tkinter as tk
from tkinter import ttk, messagebox

class FruitSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fruit Selector")
        self.geometry("300x200")

        # Label
        label = tk.Label(self, text="Select a fruit:")
        label.pack(pady=10)

        # Dropdown for Fruit Selection
        self.fruit_combobox = ttk.Combobox(self, values=["Apple", "Banana", "Cherry", "Date", "Fig", "Grape"])
        self.fruit_combobox.pack(pady=10)

        # Bind the selection event
        self.fruit_combobox.bind("<<ComboboxSelected>>", self.on_combobox_selected)

    def on_combobox_selected(self, event):
        selected_fruit = self.fruit_combobox.get()  # Get the selected fruit directly
        print(selected_fruit)  # Print the selected fruit to the console

if __name__ == "__main__":
    app = FruitSelector()
    app.mainloop()
