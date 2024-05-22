import sqlite3
import datetime

connection = sqlite3.connect("macleans.db")
cursor = connection.cursor()

#cursor.execute("create table student_details(st_num long integer, name text, formclass text, house text, dob date)")


student_details_list = [        
(24023 , "Alex Smith" ,  "12AMAT", "TK", datetime.date(2006,12,10)),
(24653 , "Tessa McLaren" ,  "12BHAH", "Hillary", datetime.date(2005,12,11)),
(24453 , "Corey Toss" ,  "13RAAH", "Rutherford", datetime.date(2004,2,29)),
(24323 , "Simon Solen" ,  "12YHAU", "Upham", datetime.date(2005,11,20)),
(24753 , "Eric Smith" ,  "11GTAH", "Snell", datetime.date(2002,12,20)),
(24133 , "Arin Dolve" ,  "13RAHR", "Rutherford", datetime.date(2007,7,4)),
(20296 , "Christian Jones", "13BEVS", "Snell", datetime.date(2006,8,29))
]

cursor.executemany("insert into student_details values (?,?,?,?,?)" , student_details_list)

#print database rows
for row in cursor.execute("select * from student_details "):
    print(row)

connection.commit()
connection.close()