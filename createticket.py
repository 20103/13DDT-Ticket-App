import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3


class CreateTicket:
    def __init__():
        top_bar_frame = tk.Frame(root, bg="green")
        top_bar_frame.grid(row=0, column=0, sticky="nsew")

        top_bar_label = tk.Label(top_bar_frame, text="Create a Ticket", bg="red")
        top_bar_label.configure(font=("", 30))
        top_bar_label.grid(row=0, column=0, padx=20, pady=10)


if __name__ == "__main__":
    root = tk.Tk()

    #Try except for ttk theme.
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    home_page = HomePage(root)
    root.mainloop()