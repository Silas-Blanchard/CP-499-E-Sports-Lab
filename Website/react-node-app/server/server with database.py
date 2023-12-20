# first of all import the socket library
import socket
import sqlite3 as sql
from datetime import datetime
import os

# variables we need outside the loop
global_computer_name = ''
global_computer_status = 0

# ======================== DATABASE STUFF ========================
# connect to the local database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "computer_status.db")
connection = sql.connect(db_path)

# create cursor object to execute sqlite3 processes
cursor = connection.cursor()

# create the database called computer_status
cursor.execute("""
                CREATE TABLE IF NOT EXISTS computer_status (
                name TEXT PRIMARY KEY,
                time_last_0_received TIMESTAMP,
                time_last_1_received TIMESTAMP
                );
                """)

# cursor.execute(f"""SELECT time_last_0_received FROM computer_status WHERE name = 'VarsityLab1';""")
# old_1 = cursor.fetchall()
# print(list(old_1))
# ======================== DATABASE STUFF ========================
# connect to the local database
connection = sql.connect("computer_status.db")

# create cursor object to execute sqlite3 processes
cursor = connection.cursor()

# create the database called computer_status
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
# ======================== DATABASE STUFF ========================


def find_computer_status(name, status):
    if status == 0:
        result_status = name + ' is in use'
    elif status == 1:
        result_status = name + ' might be in use'
    else:
        raise Exception("Invalid computer status")

    return result_status


if __name__ == '__main__':
    try:
        # next create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")

        # reserve a port on your computer in our
        # case it is 12345, but it can be anything
        port = 12345

        # Next bind to the port
        s.bind(('', port))
        print("socket bound to %s" % port)

        # put the socket into listening mode
        s.listen(3000)
        print("socket is listening")

        # a forever loop until we interrupt it or
        # an error occurs
        clients = []
        while True:
            # Establish connection with client and store it for later
            try:
                c, addr = s.accept()
                print('Got connection from', addr)
                clients.append(addr)

                # create a variable to hold the message the computer sent
                message = (c.recv(1024).decode())

                # split the message into 2 parts
                message_split = message.split(" ")

                # get the name
                global_computer_name = "".join(message_split[:-1])

                # get the status number
                global_computer_status = int(message_split[-1])

                # Print to make sure we split correctly
                print("Computer Name:", global_computer_name)
                print("Computer Status:", global_computer_status)
            except socket.error:
                print("Connection Error")
            else: #run this stuff only if it works
                # Call the function to find computer status
                set_computer_status = find_computer_status(global_computer_name, global_computer_status)
                print("Set Computer Status:", set_computer_status)

                # Inside the loop where you process each computer status
                # Insert data into the computer_status table
                # cursor.execute("INSERT or REPLACE INTO computer_status (name, time_last_0_received, time_last_1_received) VALUES (?, ?, ?)",
                #             (global_computer_name,
                #                 # Set time_last_0_received if status is 0
                #                 current_timestamp if global_computer_status == 0 else None,
                #                 # Set time_last_1_received if status is 1
                #                 current_timestamp if global_computer_status == 1 else None
                #                 ))
                if(global_computer_status): #that is, if it is a "1" which means idle
                    # Get the current timestamp
                    current_timestamp = datetime.now()

                    #some computers have alternate names
                    cursor.execute(f"""IF EXISTS (SELECT time_last_1_received FROM computer_status WHERE name = '{global_computer_name}'
                    BEGIN  
	                    UPDATE computer_status
                        SET time_last_1_received = '{current_timestamp}'
                        WHERE name = '{global_computer_name}'
                    END                                     
                    """)

                    current_timestamp = datetime.now()
                    alt_name = current_timestamp.lower()

                    #some computers have alternate names
                    cursor.execute(f"""IF EXISTS (SELECT time_last_1_received FROM computer_status WHERE name = '{alt_name}'
                    BEGIN  
	                    UPDATE computer_status
                        SET time_last_1_received = '{current_timestamp}'
                        WHERE name = '{alt_name}'
                    END                                     
                    """)
                else:
                    # Get the current timestamp
                    current_timestamp = datetime.now()

                    #some computers have alternate names
                    cursor.execute(f"""IF EXISTS (SELECT time_last_0_received FROM computer_status WHERE name = '{global_computer_name}'
                    BEGIN  
	                    UPDATE computer_status
                        SET time_last_0_received = '{current_timestamp}'
                        WHERE name = '{global_computer_name}'
                    END                                     
                    """)

                    current_timestamp = datetime.now()
                    alt_name = current_timestamp.lower()

                    #some computers have alternate names
                    cursor.execute(f"""IF EXISTS (SELECT time_last_0_received FROM computer_status WHERE name = '{alt_name}'
                    BEGIN  
	                    UPDATE computer_status
                        SET time_last_0_received = '{current_timestamp}'
                        WHERE name = '{global_computer_name}'
                    END                                     
                    """)
                # Commit the changes to the database
            finally: #everytime.
                # Close the connection with the client since this is just a ping
                connection.commit()
                c.close()

            cursor.execute("SELECT * FROM computer_status")
            myresult = cursor.fetchall()
    except Exception as e: print(e)
    # Close the database connection outside the loop
    connection.close()
