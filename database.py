import sqlite3
import os
os.system('clear')
connection = sqlite3.connect("customer.db")
cursor = connection.cursor()

#CREATE a table named customer

command1 = """CREATE TABLE IF NOT EXISTS customer (first_name text, last_name text, email text)"""

cursor.execute(command1)

cursor.execute("INSERT INTO customer VALUES ('James', 'Toptun', 'james007@gmail.com')")
cursor.execute("INSERT INTO customer VALUES ('Ben', 'Toptun', 'bengamer@gmail.com')")
cursor.execute("INSERT INTO customer VALUES ('Smart', 'Guy', 'myemail@gmail.com')")
print("Reecords added to the table")

print("--------------------------- \n Customer Table")
cursor.execute("SELECT * FROM customer")
connection.commit()
results = cursor.fetchall()
print(results)

print("===========================")
cursor.execute("SELECT * FROM customer")
connection.commit()
results = cursor.fetchall()

print(" FName" + " " + "Surname" + " " + "Email")
for item in results:
    print(item[0] + " " + item[1] + " " + item[2])
    print("\n")

cursor.close()