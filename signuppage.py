import tkinter as tk
from tkinter import ttk
import subprocess
import sqlite3

class SignUpPage:
    def __init__(self):
        root.title("Sign-Up")
        root.geometry("400x600")

        def ValidateSignup(user, pass1, pass2):
            result = [False, "No message provided"]
            if pass1 == pass2:     
                print("Passwords match")
                connection = sqlite3.connect("logins.db")
                cursor = connection.cursor()
                #Checks every row in login_details for a match.
                try:
                    cursor.execute("SELECT 1 FROM user_logins where username =?", (user,))
                    if cursor.fetchone() is not None:
                        print("Username already exists")
                        result[1] = "Username already exists"
                    else:
                        print("No duplicates found")
                        result = [True, "Account created"]
                except sqlite3.Error as e:
                    print(f"Database could not be fetched: {e}")
                    result[1] = f"Database error: {e}"
                finally:
                    connection.close()
            else:
                print("Passwords do not match.")
                result[1] = "Passwords do not match"
            return result
                
        def CreateAccount(username, password1, password2):
            feedback_widget = self.signup_feedback
            feedback_widget.grid(row=3, column=0, columnspan=2)
            Feedback = ValidateSignup(username, password1, password2)
            Success, Msg = Feedback[0], Feedback[1]
            if Success:
               connection = sqlite3.connect("logins.db")
               cursor = connection.cursor()
               try:
                    user_login = [username, password1]
                    #ERROR: Can't insert data
                    cursor.executemany("insert into user_logins values (?, ?)", user_login)
                    print("Created account")
               except sqlite3.Error as e:
                    print(f"Database could not be fetched: {e}")
                    Msg = f"Database error: {e}"
               finally:
                    connection.close()

               print("Logging in")
               root.destroy()
               subprocess.run(["python", "homepage.py"])  
               print("Home")
            feedback_widget.config(text=Msg)    

        #Configure root
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        #Widgets for credentials
        self.credentials_frame = ttk.LabelFrame(root, text="Create an account")
        self.credentials_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20, columnspan=2)

        self.username_label = ttk.Label(self.credentials_frame, text="Username")
        self.username_label.grid(row=0, column=0, sticky="nsew", padx=10)
        self.username_label.configure(font=("", 20))
        
        username_submitted = tk.StringVar()
        self.username_entry = ttk.Entry(self.credentials_frame, textvariable=username_submitted)
        self.username_entry.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.password_label = ttk.Label(self.credentials_frame, text="Password")
        self.password_label.grid(row=1, column=0, sticky="nsew", padx=10)
        self.password_label.configure(font=("", 20))

        password_submitted = tk.StringVar()
        self.password_entry = ttk.Entry(self.credentials_frame, textvariable=password_submitted)
        self.password_entry.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.password_entry.config(show="*")

        self.password_confirmation_label = tk.Label(self.credentials_frame, text="Re-enter \npassword")
        self.password_confirmation_label.grid(row=2, column=0, sticky="nsew")
        self.password_confirmation_label.configure(font=("", 15))

        password_confirmation_submitted = tk.StringVar()
        self.password_confirmation_entry = ttk.Entry(self.credentials_frame, textvariable=password_confirmation_submitted)
        self.password_confirmation_entry.grid(row=2, column=1, sticky="nsew", padx=10, pady=20)
        self.password_confirmation_entry.config(show="*")

        #Label which will display whether or not a signup is successful
        self.signup_feedback = tk.Label(self.credentials_frame, text="N/A", padx=10)

        self.signup_button = ttk.Button(self.credentials_frame, style="Accent.TButton", text="Create Account", command=lambda: CreateAccount(username_submitted.get(), password_submitted.get(), password_confirmation_submitted.get()))
        self.signup_button.grid(row=4, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    login_page = SignUpPage()
    root.mainloop()