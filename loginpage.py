#login will take us to dashboard using classes
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
       
       
def Ok():
     uname = e1.get()
     password = e2.get()
       
     if(uname == "" and password == "") :
           messagebox.showinfo("", "Blank Not allowed")
       
       
     elif(uname == "Admin" and password == "123"):        
           messagebox.showinfo("","Login Success")
           root.destroy()
           subprocess.run(["python", "homepage.py"])
       
     else :
           messagebox.showinfo("","Incorrent Username and Password")
root = tk.Tk()
root.title("Login")
root.geometry("300x200")
global e1
global e2

try:
    root.tk.call("source", "azure.tcl")
    root.tk.call("set_theme", "dark")
except Exception as e:
    print(f"Theme failed to load! Error code: {e}")
 
ttk.Label(root, text="UserName").place(x=10, y=10)
ttk.Label(root, text="Password").place(x=10, y=40)
       
e1 = ttk.Entry(root)
e1.place(x=140, y=10)
       
e2 = ttk.Entry(root)
e2.place(x=140, y=40)
e2.config(show="*")
       
       
submit_button = ttk.Button(root, text="Login", command=Ok).place(x=10, y=100)
       
root.mainloop()
