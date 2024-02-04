import sqlite3 as sql
import os

# variables we need outside the loop
global_computer_name = ''
global_computer_status = 0

# ======================== DATABASE STUFF ========================
# connect to the local database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, ".." , "html_and_layout_data" , "computer_status.db")

connection = sql.connect(data_path)

# create cursor object to execute sqlite3 processes
cursor = connection.cursor()
cursor.execute("SELECT * FROM computer_status")
myresult = cursor.fetchall()
for i in myresult:
	print(i)
connection.commit()
connection.close()
