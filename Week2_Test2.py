# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23 20:34:07 2020

@author: USUARIO
"""

#PART 1: Import the library of SQL lite Browser
import sqlite3

#PART 2: Making the connection between the Python File and...
#...the SQL Database. 
#The "Week2_Test2.sqlite" is the name of the SQL DataBase
conn = sqlite3.connect("Week2_Test3.sqlite")

#PART 3: This code allow me to handle the transmission of... 
#...information. Specificalley, it Open and Send SQL...
#...Commands  through the Cursor and then we get resopnse...
#...through the same Cursor.
cur = conn.cursor()

#PART 4.1: This code juste check if alredy exists any Table...
#... in SQLite3, and if exist, it will be deleted.
cur.execute("DROP TABLE IF EXISTS Counts")

#PART 4.2: This code create a  Table in SQLite3 called...
#...Counts with the column "email" and the column "integer"...
#...The columen integer will show the number of times...
#...appear a email in the Python File
cur.execute("""
CREATE TABLE Counts (org TEXT, count INTEGER)""")

#PART 5: In this part, the Python File will prompt for the...
#...the name of File in format TXT
fname = input("Enter file name: ")

#PART 6: In this part we will open the File in format TXT
fh = open(fname)

#PART 7: In this part we will apply a Loop through every line...
#... of the file to find the emails, then find from what...
#...organization came those emails (i.e. we olny need the...
#...part of the email that is after the "@" symbol).
for line in fh:
    if not line.startswith("From: "): continue
    pieces = line.split()
    marcaorg0 = pieces[1]
    marcaorg1 = marcaorg0.find("@")
    org = marcaorg0[marcaorg1+1:]
 
#PART 8.1: In this part we will select every email that we found...
# in the File in format TXT through the Python Code and then...
#...introduce them in the SQL Database. Specifically, this...
#...code is opening the record set in the SQL Database
#PART 8.2: Also it is important to say that the "question mark?" in the...
#...code is too avoid "SQL Injection"
#PART 8.3: (org, 1) is a Tuple
    cur.execute("SELECT count FROM Counts WHERE org = ? ", (org,))
    
#PART 9: Grab the firt information (i.e. the email) andd put it...
#...in the SQL Database
    row = cur.fetchone()
    
#PART 10: In this part of the code we check if the emai already...
#...exist in the SQL Databse, if this exists then we Update...
#...the SQL Database. If the email does not exist, then we...
#...Insert in the SQL Database.
    if row is None:
        cur.execute("""INSERT INTO Counts (org, count)
                VALUES (?, 1)""", (org,))
    else:
        cur.execute("UPDATE Counts SET count = count + 1 WHERE org = ?",
                    (org,))
        
#PART 11: It allow us to extract the info from the disk. It...
#...affect the process and make it slow if it is inside the...
#loop.
conn.commit()

#PART 12: It allow to select both colummns and order them...
#by the column "count". It is impotant to say that this...
#...order happenin SQL Database
sqlstr = "SELECT org, count FROM Counts ORDER BY count"

#PART 13: Last, print in Python the Table (i.e. the same...
#...Table of SQL Database.
for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])

#PART 14: Apparently this is the close of the transmission of...
#...data between python and SQL Database.
cur.close()

#IMPORTANT: to no not lose data, it is important to do right click in...
#...the link and then do the save link (ie. "savee link as")