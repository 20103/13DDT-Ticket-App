import tkinter as tk
from tkinter import ttk
import sqlite3

class HomePage:
    #Initialisation
    def __init__(self, root):
        root.title("Home")
        root.geometry("500x600")

        #Two distinct sections: Top Bar and Ticket Actions.
        top_bar_frame = tk.Frame(root, width=100, height=50)
        top_bar_frame.grid(row=0, column=0, sticky="nsew")

        top_bar_label = tk.Label(top_bar_frame, text="Home")
        top_bar_label.configure(font=("", 30))
        top_bar_label.grid(row=0, column=0, padx=20, pady=10)

        main_body_frame = ttk.LabelFrame(root, width=100, height=300, borderwidth=10, text="Tickets")
        main_body_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        #Scale widgets appropriately according to window size.
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)

        #Create a tree to display ticket information.
        ticket_tree_columns = ("venue", "time_created", "wait_time")

        ticket_tree = ttk.Treeview(main_body_frame, columns=ticket_tree_columns, show="headings")
        ticket_tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        #Scale widgets again.
        main_body_frame.grid_columnconfigure(0, weight=1)
        main_body_frame.grid_rowconfigure(0, weight=1)

        #Create the treeview headings
        ticket_tree.heading("venue", text="Venue")
        ticket_tree.heading("time_created", text="Time Created")
        ticket_tree.heading("wait_time", text="Estimated Wait Time")

        #Initialise and access db holding ticket information.
        connection = sqlite3.connect("tickets.db")
        cursor = connection.cursor()

        #Example code in basic table form.
        """tickets = [
            ("McDonalds", "9:15pm", "20 Minutes"), 
            ("Burger King", "1 Hour ago", "30 Seconds"), 
            ("Macleans College", "2 Days ago", "Now"), 
            ("Countdown", "14/05/2024 09:57 PM", "1 Hour")]
        
        for ticket in tickets:
            ticket_tree.insert(ticket)"""

        #Insert each row from db into the treeview.
        for ticket_detail in cursor.execute("select * from ticket_details"):
            ticket_tree.insert('', tk.END, values=ticket_detail)

        #End db connection.
        connection.commit()
        connection.close()

        create_ticket_button = ttk.Button(main_body_frame, text="Create A Ticket", style="Accent.TButton")
        create_ticket_button.grid(row=1, column=0, pady=20, sticky="nsew")


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

#hi