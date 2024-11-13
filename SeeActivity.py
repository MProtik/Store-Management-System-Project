import tkinter as tk
from tkinter import messagebox
import logging

# Configure logging to write to app.log with hour and minute format
logging.basicConfig(
    level=logging.INFO,
    filename="app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%H:%M"  # Only hours and minutes
)
logger = logging.getLogger("log")

# Sample log generation for testing purposes
# Log messages to app.log for debugging
# logger.info("Application started.")
# logger.info("Another log entry.")

class LogViewerApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Add a label to show activity logs
        log_label = tk.Label(self, text="Activity Logs", font=("Arial", 16))
        log_label.pack(pady=10)

        # Create a Text widget to display logs
        self.log_text = tk.Text(self, height=45, width=130, wrap=tk.WORD, state=tk.DISABLED, font=("Arial", 12))
        self.log_text.pack(padx=10, pady=10)

        # Load the logs from "app.log" initially
        self.load_logs()

    def load_logs(self):
        """Load logs from the file and display them in the Text widget."""
        try:
            with open("app.log", "r") as log_file:
                logs = log_file.read()
                self.display_logs(logs)
        except FileNotFoundError:
            messagebox.showerror("Error", "Log file not found.")

    def display_logs(self, logs):
        """Display the logs in the Text widget."""
        self.log_text.config(state=tk.NORMAL)  # Enable editing to insert text
        self.log_text.delete(1.0, tk.END)  # Clear existing text
        self.log_text.insert(tk.END, logs)  # Insert logs into the Text widget
        self.log_text.config(state=tk.DISABLED)  # Disable editing after inserting


class StoreManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Store Management System")
        self.geometry("900x600")

        # Create a frame for the main content
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Initialize the activity page (LogViewerApp) but keep it hidden initially
        self.activity_page = LogViewerApp(self.main_frame)
        self.activity_page.pack_forget()

        # Create a button to show the "See Activity" page
        activity_button = tk.Button(self, text="See Activity", command=self.show_activity)
        activity_button.pack(pady=10)

        # Create another button to hide the activity page (e.g., "Hide Activity")
        hide_activity_button = tk.Button(self, text="Hide Activity", command=self.hide_activity)
        hide_activity_button.pack(pady=10)

    def show_activity(self):
        """Show the activity (log viewer) page in full screen and refresh logs."""
        self.activity_page.load_logs()  # Refresh the logs
        self.attributes("-fullscreen", True)  # Set window to fullscreen
        self.activity_page.pack(expand=True, fill="both")  # Show the activity page

    def hide_activity(self):
        """Hide the activity (log viewer) page and return to normal window mode."""
        self.activity_page.pack_forget()  # Hide the activity page
        self.attributes("-fullscreen", False)  # Exit fullscreen mode

if __name__ == "__main__":
    app = StoreManagementApp()
    app.mainloop()
