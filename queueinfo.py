import tkinter as tk
from tkinter import ttk, font
import subprocess, sqlite3, json, time
from datetime import datetime


class JoinQueue:
    def __init__(self, root):
        #Configure root
        root.wm_iconbitmap('ticket.ico')
        root.title("Queue")
        root.geometry("450x400")

        def CreateTicket():
            root.destroy()
            subprocess.run(["python", "createticket.py"])

        def GetCurrentUser():
            with open("settings.json", mode="r", encoding="utf-8") as openfile:
                json_object = json.load(openfile)
                current_user = json_object.get("username")

                return current_user
        
        def LeaveQueue():
            feedback_widget.grid(row=4, column=0)

            username = GetCurrentUser()

            print(username)

            try:
                #Attempts to delete said row from database and tableview.
                with sqlite3.connect("main.db") as connection:
                    cursor = connection.cursor()
                    rows_affected = cursor.execute("DELETE FROM queue WHERE username = ?", (username,)).rowcount

                    if rows_affected == 0:
                        print("Username not found")
                        feedback_widget.config(text="You are not in the queue!")
                        return
                    connection.commit()
            except sqlite3.Error as e:
                    print(f"Database error: {e}")
            else:
                connection.commit()
                #Update the table
                # Clear the entire tree before inserting new items
                for item in ticket_tree.get_children():
                    ticket_tree.delete(item)
                
                for ticket_detail in cursor.execute("select * from queue"):
                    ticket_tree.insert('', tk.END, values=ticket_detail)

                #Close the connection.
                connection.close()

                feedback_widget.config(text="Successfully left the queue!")
            return

        def EnterQueue(): 
            current_time = datetime.now()

            formatted_time = current_time.strftime('%I:%M %p')
            queue_info = [GetCurrentUser(), formatted_time]

            feedback_widget.grid(row=4, column=0)

            try:
                with sqlite3.connect("main.db") as connection:
                    cursor = connection.cursor()

                    # Attempts to enter queue with given information
                    cursor.executemany("insert into queue values (?, ?)", (queue_info,))
                    connection.commit()
            except sqlite3.Error as e:
                if "UNIQUE constraint failed" in str(e):
                    print("Database error: Unique constraint failed")
                    feedback_widget.config(text="You are already in the queue!")
                    return
                else:
                    print(f"Database error: {e}")
            else:
                connection.commit()
                #Update the table
                # Clear the entire tree before inserting new items
                for item in ticket_tree.get_children():
                    ticket_tree.delete(item)

                for ticket_detail in cursor.execute("select * from queue"):
                    ticket_tree.insert('', tk.END, values=ticket_detail)
                #Close the connection.
                connection.close()

                feedback_widget.config(text="Successfully joined the queue!")
            return                
   
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

        join_queue_button = ttk.Button(main_frame, text="Enter the queue with current information", style="Accent.TButton", command=EnterQueue)
        join_queue_button.grid(row=1, column=0, pady=10)

        leave_queue_button = ttk.Button(main_frame, text="Leave the queue", command=LeaveQueue)
        leave_queue_button.grid(row=2, column=0)

        back_button = ttk.Button(main_frame, text="Go back", command=CreateTicket)
        back_button.grid(row=3, column=0, pady=20)

        feedback_widget = ttk.Label(main_frame, text="HELLO")


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