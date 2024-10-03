import tkinter as tk
from tkinter import messagebox

def dashboard_page():
    dashboard_window = tk.Toplevel()
    dashboard_window.title("Dashboard")
    dashboard_window.geometry("400x300")

    total_stock_label = tk.Label(dashboard_window, text="Total Stock: 100")
    total_stock_label.pack(pady=20)

    vendor_count_label = tk.Label(dashboard_window, text="Vendors: 5")
    vendor_count_label.pack(pady=20)

    recent_activity_label = tk.Label(dashboard_window, text="Recent Activity: Product X added")
    recent_activity_label.pack(pady=20)
