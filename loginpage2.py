import tkinter as tk
from tkinter import ttk

class LoginPage:
    def __init__(self, root):
        root.title("Login")
        root.geometry("300x600")

        #Widgets for credentials
        credentials_frame = ttk.LabelFrame(root, text="Please enter your credentials.")
        credentials_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20, columnspan=2)

        credentials_frame.grid_columnconfigure(0, weight=1)
        credentials_frame.grid_rowconfigure(0, weight=1)

        username_label = ttk.Label(credentials_frame, text="Username")
        username_label.grid(row=0, column=0, sticky="ew")
        username_label.configure(font=("", 20))

        username_entry = ttk.Entry(credentials_frame)
        username_entry.grid(row=0, column=1, sticky="ew")

        password_label = ttk.Label(credentials_frame, text="Password")
        password_label.grid(row=1, column=0, sticky="ew")
        password_label.configure(font=("", 20))

        password_entry = ttk.Entry(credentials_frame)
        password_entry.grid(row=1, column=1, sticky="ew")

if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    login_page = LoginPage(root)
    root.mainloop()


