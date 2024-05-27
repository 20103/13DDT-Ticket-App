import sqlite3
connection = sqlite3.connect("logins.db")
cursor = connection.cursor()

#Similarly to ticket_db, initialises the db if it doesn't already exist and inserts dummy values for testing.
create_table_command = """CREATE TABLE IF NOT EXISTS user_logins (username text, password text)"""

#Inserts rows of table into db.
cursor.execute(create_table_command)


#Dummy values.
#Also, consider linking logins with ticket. Either as two separate dbs, or a table in one?
"""logins = [
    ("Admin", "1234"), 
    ("User1", "password"),
    ("catlover", "ilovecats")]"""


#cursor.executemany("insert into user_logins values (?,?)" , logins)

#Prints out values from db.
for row in cursor.execute("select * from user_logins"):
    print(row)

#Save and close the connection.
connection.commit()
connection.close()