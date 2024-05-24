import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3

class SignUpPage:
    def __init__(self, root):
        root.title("Sign-Up")
        root.geometry("400x600")

        test = ttk.Frame(root)


if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    login_page = SignUpPage(root)
    root.mainloop()