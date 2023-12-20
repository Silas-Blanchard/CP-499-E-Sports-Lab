import sqlite3
from datetime import datetime, timedelta
import random

# Connect to the local database
connection = sqlite3.connect("test_database.db")

# Create cursor object to execute SQLite processes
cursor = connection.cursor()

# Create the database table if it doesn't exist
cursor.execute("""
                CREATE TABLE IF NOT EXISTS use_database (
                name TEXT PRIMARY KEY, 
                time_last_0_received TIMESTAMP,
                time_last_1_received TIMESTAMP
                )
                """)

# Commit changes and close the connection
connection.commit()
connection.close()

# Add 9 computers with random times
for i in range(1, 16):
    computer_name = f'Computer{i:02d}'
    random_time_0 = datetime.now() - timedelta(minutes=random.randint(1, 60))
    random_time_1 = datetime.now() - timedelta(minutes=random.randint(1, 60))

    cursor.execute("""
                   INSERT OR REPLACE INTO test_database (name, time_last_0_received, time_last_1_received) 
                   VALUES (?, ?, ?)
                   """, (computer_name, random_time_0, random_time_1))

# Add 3 computers with specific statuses
cursor.execute("""
               INSERT OR REPLACE INTO test_database (name, time_last_0_received, time_last_1_received) 
               VALUES (?, ?, ?)
               """, ('InUseComputer', datetime.now(), None))

cursor.execute("""
               INSERT OR REPLACE INTO test_database (name, time_last_0_received, time_last_1_received) 
               VALUES (?, ?, ?)
               """,
               ('PossiblyInUseComputer', datetime.now(), datetime.now() - timedelta(minutes=random.randint(20, 30))))

cursor.execute("""
               INSERT OR REPLACE INTO test_database (name, time_last_0_received, time_last_1_received) 
               VALUES (?, ?, ?)
               """, ('NotInUseComputer', '2023-12-05 9:30:0.000000', '2023-12-05 9:30:0.000000'))

# Commit changes and close the connection
connection.commit()
connection.close()
