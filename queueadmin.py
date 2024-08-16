import tkinter as tk
from tkinter import ttk
import subprocess, sqlite3, json
from datetime import datetime


class JoinQueue:
    def __init__(self, root):
        #Root Config

        root.wm_iconbitmap('ticket.ico')
        root.title("Manage queue")
        root.geometry("450x400")

        def CreateTicket():
            root.destroy()
            subprocess.run(["python", "createticket.py"])

        """def GetCurrentUser():
            with open("settings.json", mode="r", encoding="utf-8") as openfile:
                json_object = json.load(openfile)
                print(json_object)
                currentUser = json_object.get("username")

                return currentUser"""
        
        def DeleteSelectedUser():
            feedback_widget.grid(row=3, column=0)

            selected_user = ticket_tree.selection()

            print(selected_user)

            if not selected_user:
                print("No user has been selected!")
                feedback_widget.config(text="No user selected!")
                return  
            
            for selected in selected_user:
                item = ticket_tree.item(selected)
                username = item['values'][0]
                time_created = item['values'][1]

                try:
                    #Attempts to delete said row from database and tableview.
                    with sqlite3.connect("main.db") as connection:
                        cursor = connection.cursor()
                        cursor.execute("DELETE FROM queue WHERE username = ? AND time_created = ?", (username, time_created))

                    ticket_tree.delete(selected)
                    feedback_widget.config(text="User removed successfully!")

                except sqlite3.Error as e:
                        feedback_widget.config(text=f"Failed to remove user: {e}")
                        print(f"Database error: {e}")
                    
                else:
                    #Commit and close connection
                    connection.commit()
                    connection.close()

            
   
   
         #Configure root
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)

        top_bar_frame = tk.Frame(root, bg="green")
        top_bar_frame.grid(row=0, column=0, sticky="nsew")

        main_frame = tk.LabelFrame(root, text="Queue")
        main_frame.grid(row=1, column=0)

        ticket_tree_columns = ("username", "time_created")

        ticket_tree = ttk.Treeview(main_frame, columns=ticket_tree_columns, show="headings")
        ticket_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #Scale widgets again.
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        #Create the treeview headings
        ticket_tree.heading("username", text="Username")
        ticket_tree.heading("time_created", text="Time Created")
        #ticket_tree.heading("wait_time", text="Estimated Wait Time")

        #Initialise and access db holding ticket information.
        connection = sqlite3.connect("main.db")
        cursor = connection.cursor()

        #Insert each row from db into the treeview.
        for ticket_detail in cursor.execute("select * from queue"):
            ticket_tree.insert('', tk.END, values=ticket_detail)
        
        connection.close()

        remove_selected_user = ttk.Button(main_frame, text="Remove selected user", command=DeleteSelectedUser)
        remove_selected_user.grid(row=1, column=0)

        back_button = ttk.Button(main_frame, text="Go back", style="Accent.TButton", command=CreateTicket)
        back_button.grid(row=2, column=0, pady=20)

        feedback_widget = ttk.Label(main_frame, text="An error occured. No modifications have been made.")


if __name__ == "__main__":
    root = tk.Tk()

    #Try except for ttk theme.
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    home_page = JoinQueue(root)
    root.mainloop()