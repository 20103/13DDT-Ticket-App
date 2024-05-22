import sqlite3
connection = sqlite3.connect("tickets.db")
cursor = connection.cursor()

#CREATE a table named customer

create_table_command = """CREATE TABLE IF NOT EXISTS ticket_details (venue text, time_created text, wait_time text)"""

cursor.execute(create_table_command)

tickets = [
    ("McDonalds", "9:15pm", "20 Minutes"), 
    ("Burger King", "1 Hour ago", "30 Seconds"), 
    ("Macleans College", "2 Days ago", "Now"), 
    ("Countdown", "14/05/2024 09:57 PM", "1 Hour")]


cursor.executemany("insert into ticket_details values (?,?,?)" , tickets)

for row in cursor.execute("select * from ticket_details"):
    print(row)

connection.commit()
cursor.close()