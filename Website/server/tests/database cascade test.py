import sqlite3
from datetime import datetime, timedelta
import random
import time
import os

# Connect to the local database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
connect_path = os.path.join(BASE_DIR, ".." ,"html_and_layout_data" , "computer_status.db")
connection = sqlite3.connect(connect_path)

# Create cursor object to execute SQLite processes
cursor = connection.cursor()

# Create the database table if it doesn't exist
# cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS test_database (
#                 name TEXT PRIMARY KEY, 
#                 time_last_0_received TIMESTAMP,
#                 time_last_1_received TIMESTAMP
#                 )
#                 """)

#Takes every computer and updates its color for the sake of testing
cursor.execute("SELECT name FROM computer_status")
comps = cursor.fetchall()
print(cursor.fetchall())
for row in comps:
    now = datetime.now()
    comp_name = row[0]
    #thirty_one_minutes_ago is for our last idle ping
    #this should make it so that each computer is definitely in use
    thirty_minutes_ago =  datetime.now() - timedelta(minutes=45)
    cursor.execute(f"""
                    UPDATE computer_status
                    SET time_last_0_received = '{now}', time_last_1_received = '{now}'
                    WHERE name = '{comp_name}';
                    """)
connection.commit()
cursor.execute("SELECT * FROM computer_status WHERE name = 'InUseComputer'")
print(cursor.fetchall())
time.sleep(1)
    
for row in comps:
    now = datetime.now()

    #thirty_one_minutes_ago is for our last idle ping
    #this should make it so that each computer is definitely on
    ten_minutes_ago =  datetime.now() - timedelta(minutes=45)
    comp_name = row[0]
    cursor.execute(f"""
                    UPDATE computer_status
                    SET time_last_0_received = '{now}', time_last_1_received = '{ten_minutes_ago}'
                    WHERE name = '{comp_name}';
                    """)
# Commit changes and close the connection
connection.commit()
connection.close()
