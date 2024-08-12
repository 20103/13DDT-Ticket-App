import tkinter as tk
from tkinter import ttk, font
import subprocess, random, string, qrcode

class CreateTicket:

    def __init__(self, root):
        QR_NUMBER_LENGTH = 20

        def JoinQueue():
            #Destroys this instance and starts new process of queue.py
                root.destroy()
                subprocess.run(["python", "queueinfo.py"])
                print("Success")

        def GenerateTicket():

            #Instead of generating a unique number and storing that, perhaps make it so the business has a unique QR code that is tied with their business account. When a customer account scans the QR code, they can see business information such as the queue length and average wait time. They will also be able to join the queue by signging into their account, and see live feedback on the mobile app.
            generated_ticket = ''.join(random.choices(string.ascii_uppercase + string.digits, k=QR_NUMBER_LENGTH))
            info_label.configure(text="Your unique business code is:")

            img = qrcode.make(generated_ticket)

            img.save("generated_qr_code.png")


            ticket_number_label.grid(row=3, sticky="nsew")
            ticket_number_label.configure(text=generated_ticket)

            #Probably save the QR code with the rest of the information in the DB


         #Configure root
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=1)

        top_bar_frame = tk.Frame(root, bg="green")
        top_bar_frame.grid(row=0, column=0, sticky="nsew")

        top_bar_label = tk.Label(top_bar_frame, text="Create a Ticket", bg="red")
        top_bar_label.configure(font=("", 30))
        top_bar_label.grid(row=0, column=0, padx=20, pady=10)

        main_frame = tk.LabelFrame(root, text="Tickets")
        main_frame.grid(row=1, column=0)

        info_label = tk.Label(main_frame, text="You are not in a queue.\nClick the button below to generate a ticket")
        info_label.configure(font=("", 15))
        info_label.grid(row=2, column=0, padx=10, pady=10)

        ticket_number_label = tk.Label(main_frame, font=(font.Font(family="Consolas", size=20, weight="bold")))

        info_label2 = ttk.Label(main_frame)

        create_ticket_button = ttk.Button(main_frame, text="Create a ticket", style="Accent.TButton", command=GenerateTicket)
        create_ticket_button.grid(row=4, column=0, padx=20, pady=20)

        join_queue_button = ttk.Button(main_frame, text="Join the queue", command=JoinQueue)
        join_queue_button.grid(row=5, column=0, padx=10, pady=10)



if __name__ == "__main__":
    root = tk.Tk()

    #Try except for ttk theme.
    try:
        root.tk.call("source", "azure.tcl")
        root.tk.call("set_theme", "dark")
    except Exception as e:
        print(f"Theme failed to load! Error code: {e}")
    
    home_page = CreateTicket(root)
    root.mainloop()