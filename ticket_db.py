import sqlite3
connection = sqlite3.connect("tickets.db")
cursor = connection.cursor()

#Similarly to login_db, initialises the db if it doesn't already exist and inserts dummy values for testing.
create_table_command = """CREATE TABLE IF NOT EXISTS ticket_details (venue text, time_created text, wait_time text)"""

#Executes the SQL code.
cursor.execute(create_table_command)

#Dummy values.
tickets = [
    ("McDonalds", "9:15pm", "20 Minutes"), 
    ("Burger King", "1 Hour ago", "30 Seconds"), 
    ("Macleans College", "2 Days ago", "Now"), 
    ("Countdown", "14/05/2024 09:57 PM", "1 Hour")]

#Inserts rows of table into db.
cursor.executemany("insert into ticket_details values (?,?,?)" , tickets)

#Prints out values from db
for row in cursor.execute("select * from ticket_details"):
    print(row)

#Save and close the connection.
connection.commit()
connection.close()