import tkinter as tk
from tkinter import ttk
import subprocess, sqlite3, json
from passlib.hash import pbkdf2_sha256

class LoginPage:

    def ModifyUser(newuser):
            #Accesses and reads the JSON file which holds the current username
            with open('settings.json', 'r') as f:
                json_data = json.load(f)
            field_key = "username"
            if field_key in json_data:
                json_data[field_key] = newuser

            #Updates username
            with open('settings.json', 'w') as f:
                json.dump(json_data, f, indent=4)
    
    def __init__(self, root):

        root.wm_iconbitmap('ticket.ico')
        root.title("Login")
        root.geometry("400x400")
        
        #Validates the login by comparing with db
        def ValidLogin():
            print(f"Submitted Username: {username_submitted.get()} \nSubmitted Password:{password_submitted.get()}")
            #Initialise and access db holding login information.
            connection = sqlite3.connect("main.db")
            cursor = connection.cursor()
            #Checks every row in login_details for a match.
            for login_detail in cursor.execute("select * from user_logins"):
                #Makes sure username entered exist, and the password submitted matches the hash.
                if login_detail[0] == username_submitted.get() and pbkdf2_sha256.verify(password_submitted.get(), login_detail[1]):
                    LoginPage.ModifyUser(login_detail[0])
                    return True
            return False


        #Function which handles login attempt.       
        def Login(event=None):
            login_feedback.grid(row=2, column=0, columnspan=2)
            #Credentials match
            if ValidLogin():
                login_feedback.config(text="Login successful!", fg="green")
                #Destroys this instance and starts new process of homepage.py
                root.destroy()
                subprocess.run(["python", "homepage.py"])
                print("Success")
            #Credentials do not match. Perhaps consider adding personalised information? e.g. This username does not exist, Password hint: 2 Numbers. However, consider security implications.
            else:
                login_feedback.config(text="Please check your credentials.", fg="red")
                print("Fail")
            #Clears both entry, doubles as active user feedback.
            password_entry.delete(0, "end")

        root.bind('<Return>', Login)

        def SignUp():
            root.destroy()
            subprocess.run(["python", "signuppage.py"])
            print("Sign-Up")


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
        login_feedback = tk.Label(credentials_frame, text="N/A", padx=10)

        submit_button = ttk.Button(credentials_frame, text="Login", style="Accent.TButton", command=Login)
        submit_button.grid(row=3, column=0, padx=10, pady=10, sticky="nsew", columnspan=2)

        signup_button = ttk.Button(credentials_frame, text="Sign-Up", command=SignUp)
        signup_button.grid(row=4, column=0, padx=10, pady=10, columnspan=2)


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


