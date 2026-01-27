"""
Security Toolkit - Main Entry Point
Launches the integrated security testing application
"""

import tkinter as tk
from ui.app import SecurityToolkit


def main():
    """Initialize and run the application"""
    # Create main window
    root = tk.Tk()

    # Initialize application
    app = SecurityToolkit(root)

    # Start event loop
    root.mainloop()


if __name__ == "__main__":
    main()