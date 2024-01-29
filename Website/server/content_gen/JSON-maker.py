#this file is for making JSON's from the  database very nice
from ComputerStatusUpdater import computer_status_update
import json
import os
import sqlite3

#connecting to database using objective path so nothing gets confused
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, ".." , "html_and_layout_data", "computer_status.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

json_path = os.path.join(BASE_DIR, "colors.json")

cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM computer_status")
rows = cursor.fetchall()

dictionary = {}
for row in rows:
    computer_name = row[0]
    time_last_0_received = row[1]
    time_last_1_received = row[2]
    #what determines color
    status, time_status = computer_status_update(computer_name, time_last_0_received, time_last_1_received)

# which color we are using
    if "is not in use" in status:
        box_color = "#228C22"
    elif "might be in use" in status:
        box_color = "#D09B2C"
    elif "is in use" in status:
        box_color = "#801B1B"

    dictionary[computer_name] = box_color

print(dictionary)

#superfluous
f = open(json_path, "w")
json.dump(dictionary, f)
f.close()
