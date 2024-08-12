import tkinter as tk
from tkinter import ttk
import subprocess, sqlite3
from password_strength import PasswordPolicy
from passlib.hash import pbkdf2_sha256


class SignUpPage:
    def __init__(self):
        root.title("Sign-Up")
        root.geometry("400x400")

        def Login():
            root.destroy()
            subprocess.run(["python", "loginpage.py"])

        #Password hashing function
        def HashPassword(plaintext):
            #Debugging
            print(f"Password hash = {pbkdf2_sha256.hash(plaintext)}")
            return pbkdf2_sha256.hash(plaintext)
        
        def ValidString(str):
            return not str.isspace() and len(str) > 0
        
        #Function which begins the process of validating signup information.
        def ValidateSignup(user, pass1, pass2):

            PASSWORD_POLICY = PasswordPolicy.from_names(
                length=8,
                uppercase=1,
                numbers=1,
            )

            if not ValidString(user):
                #If username is empty
                print("Please enter a username")
                return [False, "Please enter a username"]

            if pass1 != pass2:
                #If passwords do not match, stays Falsey
                print("Passwords do not match")
                return [False, "Passwords do not match"]
            
            if not ValidString(pass1):
                #If password is empty
                print("Password must not be empty.")
                return [False, "Password must not be empty"] 
            
            if " " in pass1:
                print("Password contains whitespace")  
                return [False, "Password must not contain any whitespace"]

            if PASSWORD_POLICY.test(pass1):
                #Password does not meet at least 1 condition
                print("A password condition was not met")
                #This variable is assigned a tuple of conditions which are not met
                failed_conditions = PASSWORD_POLICY.test(pass1)
                print(failed_conditions)

                #Default message
                conditions_message = "Your password must meet the following conditions:"
                #Iterates over every failed condition in failed_conditions tuple, and concatenates them to the default message.
                for condition in failed_conditions:
                    conditions_message += f"\n- {condition}"
                return [False, conditions_message]

            return [True, "No message provided"]
                
                
        def CreateAccount(username, password1, password2):
            feedback_widget = self.signup_feedback
            feedback_widget.grid(row=4, column=0, columnspan=2)
            Feedback = ValidateSignup(username, password1, password2)
            Success, Msg = Feedback[0], Feedback[1]
            if Success:
               #ValidateSignup() function returns true, continue with account creation
               connection = sqlite3.connect("main.db")
               cursor = connection.cursor()
               try:
                    #Organises account data into a table, which is then inserted into the user_logins table.
                    user_login = [username, HashPassword(password1)]
                    cursor.executemany("insert into user_logins values (?, ?)", (user_login,))
                    print("Created account")
               except sqlite3.Error as e:
                    if "UNIQUE constraint failed" in str(e):
                        print("Database error: Unique constraint failed")
                        feedback_widget.config(text="This username already exists")
                        return
                    else:
                        print(f"Database error: {e}")
               finally:
                    #Commit all changes and close the connection.
                    connection.commit()
                    connection.close()

               print("Account created")
               #Destroys window and opens homepage.py
               root.destroy()
               subprocess.run(["python", "loginpage.py"])  
               print("Login page")
            #Message changes depending on feedback given.
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

        """password_requirement = ttk.Label(self.credentials_frame, text="Your password must contain:\nAt least 8 characters")
        password_requirement.grid(row=2, column=1)"""

        self.password_confirmation_label = tk.Label(self.credentials_frame, text="Re-enter \npassword")
        self.password_confirmation_label.grid(row=3, column=0, sticky="nsew")
        self.password_confirmation_label.configure(font=("", 15))

        password_confirmation_submitted = tk.StringVar()
        self.password_confirmation_entry = ttk.Entry(self.credentials_frame, textvariable=password_confirmation_submitted)
        self.password_confirmation_entry.grid(row=3, column=1, sticky="nsew", padx=10, pady=20)
        self.password_confirmation_entry.config(show="*")

        #Label which will display whether or not a signup is successful
        self.signup_feedback = tk.Label(self.credentials_frame, text="N/A", padx=10)

        self.signup_button = ttk.Button(self.credentials_frame, style="Accent.TButton", text="Create Account", command=lambda: CreateAccount(username_submitted.get(), password_submitted.get(), password_confirmation_submitted.get()))
        self.signup_button.grid(row=5, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)

        self.login_button = ttk.Button(self.credentials_frame, text="Go back to login page", command=Login)
        self.login_button.grid(row=6, column=0, columnspan=2)


if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    login_page = SignUpPage()
    root.mainloop()