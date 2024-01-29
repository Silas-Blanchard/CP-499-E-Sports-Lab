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
cursor.execute("DROP TABLE IF EXISTS computer_status")
connection.commit()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS computer_status (
                name TEXT PRIMARY KEY,
                time_last_0_received TIMESTAMP,
                time_last_1_received TIMESTAMP,
                reserved_start TIMESTAMP,
                reserved_end TIMESTAMP,
                is_out_of_order
                )
                """)

connection = sql.connect(data_path)
cursor = connection.cursor()

for i in range(1,13):
    cursor.execute("INSERT or REPLACE INTO computer_status (name, time_last_0_received, time_last_1_received) VALUES (?, ?, ?)",
        ("VarsityLab" + str(i),
        # Set time_last_0_received if status is 0
        None,
        # Set time_last_1_received if status is 1
        None
        ))

for i in range(1,7):
    cursor.execute("INSERT or REPLACE INTO computer_status (name, time_last_0_received, time_last_1_received) VALUES (?, ?, ?)",
        ("EventSpace" + str(i),
        # Set time_last_0_received if status is 0
        None,
        # Set time_last_1_received if status is 1
        None
        ))

connection.commit()
connection.close()
