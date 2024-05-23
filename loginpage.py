import tkinter as tk
from tkinter import ttk
import subprocess

class LoginPage:
    def __init__(self, root):
        root.title("Login")
        root.geometry("400x600")


        username = "admin"
        password = "1234"

        def Login(event=None):
            login_feedback.grid(row=2, column=0, columnspan=2)
            if username_submitted.get() == username and password_submitted.get() == password:
                login_feedback.config(text="Login successful!", fg="green")
                #Destroys this instance and starts new process of homepage.py
                root.destroy()
                subprocess.run(["python", "homepage.py"])
                print("Success")
            else:
                login_feedback.config(text="Your credentials are incorrect", fg="red")
                print("Your credentials are incorrect")
            #Clears both entry, doubles as active user feedback.
            username_entry.delete(0, "end")
            password_entry.delete(0, "end")

        root.bind('<Return>', Login)
        #Configure root
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        #Widgets for credentials
        credentials_frame = ttk.LabelFrame(root, text="Please enter your credentials")
        credentials_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20, columnspan=2)


        username_label = ttk.Label(credentials_frame, text="Username")
        username_label.grid(row=0, column=0, sticky="nsew", padx=10)
        username_label.configure(font=("", 20))
        
        username_submitted = tk.StringVar()
        username_entry = ttk.Entry(credentials_frame, textvariable=username_submitted)
        username_entry.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        password_label = ttk.Label(credentials_frame, text="Password")
        password_label.grid(row=1, column=0, sticky="nsew", padx=10)
        password_label.configure(font=("", 20))

        password_submitted = tk.StringVar()
        password_entry = ttk.Entry(credentials_frame, textvariable=password_submitted)
        password_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        password_entry.config(show="*")

        #Label which will display whether or not a login is successful
        login_feedback = tk.Label(credentials_frame, text="hi", padx=10)

        submit_button = ttk.Button(credentials_frame, text="Login", style="Accent.TButton", command=Login)
        submit_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)
        submit_button.configure()

#Main
if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    login_page = LoginPage(root)
    root.mainloop()


