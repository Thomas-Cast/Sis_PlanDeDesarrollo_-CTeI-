"""
main.py
Punto de entrada.
"""

import tkinter as tk
from app_gui import App


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()