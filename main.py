"""
main.py
Punto de entrada para ejecutar la aplicación.
Solo importa y lanza la interfaz gráfica.
"""

from app_gui import App
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()