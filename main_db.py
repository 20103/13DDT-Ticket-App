import sqlite3
from passlib.hash import pbkdf2_sha256

connection = sqlite3.connect("main.db")
cursor = connection.cursor()

#Similarly to ticket_db, initialises the db if it doesn't already exist and inserts dummy values for testing.
#create_table_command = """CREATE TABLE IF NOT EXISTS user_logins (username text, password text)"""

create_table_command = """CREATE TABLE IF NOT EXISTS user_logins (username text, password text)"""

#Inserts rows of table into db.
cursor.execute(create_table_command)

cursor.execute("""CREATE TABLE IF NOT EXISTS queue (username text, code text)""")


#Dummy values.
#Also, consider linking logins with ticket. Either as two separate dbs, or a table in one?
"""logins = [
    ("Admin", "1234"), 
    ("User1", "password"),
    ("catlover", "ilovecats")]"""


#cursor.executemany("insert into user_logins values (?,?)" , logins)

#Prints out values from db.
local_logins = []

for row in cursor.execute("select * from user_logins"):
    list.append(local_logins, row)

for row in local_logins:
    #not sure how reliable this is, but it works
    if "$pbkdf2" not in row[1]:
        print(row[1] + " is not a valid hash! Re-writing and converting to SHA256 hash...")
        new_hash = pbkdf2_sha256.hash(row[1])
        print(f"New Password hash = {new_hash}\n")
        cursor.execute(f"""UPDATE user_logins SET password='{new_hash}' WHERE password='{row[1]}';""") #SQL injection :(
        continue
    else:
        print(row[1] + "is a valid hash! Skipping \n")


#Save and close the connection.
connection.commit()
connection.close()