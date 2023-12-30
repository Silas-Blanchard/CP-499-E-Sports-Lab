import sqlite3
from datetime import datetime


# Function to convert seconds to a human-readable format
def format_time(seconds):
    # Convert seconds to minutes and remaining seconds
    minutes, seconds = divmod(seconds, 60)

    # Convert minutes to hours and remaining minutes
    hours, minutes = divmod(minutes, 60)

    # Check if there are hours, minutes, or only seconds
    if hours > 0:
        # Format the time as hours and minutes
        return f"{int(hours)} hours and {int(minutes)} minutes"
    elif minutes > 0:
        # Format the time as only minutes
        return f"{int(minutes)} minutes"
    else:
        # Format the time as only seconds
        return f"{int(seconds)} seconds"


# Status update function
def computer_status_update(computer_name, time_last_0_received_str, time_last_1_received_str):
    # Get the current time
    time_now = datetime.now()

    # Convert timestamp strings to datetime objects if they are not None
    time_last_0_received = datetime.strptime(time_last_0_received_str,
                                             "%Y-%m-%d %H:%M:%S.%f") if time_last_0_received_str else None
    time_last_1_received = datetime.strptime(time_last_1_received_str,
                                             "%Y-%m-%d %H:%M:%S.%f") if time_last_1_received_str else None

    # Initialize time_status with a default value
    time_status = "Time status not available"

    # Check computer status based on timestamps
    if time_last_0_received and (time_now - time_last_0_received).total_seconds() < (60 * 5):
        if time_last_1_received and (time_now - time_last_1_received).total_seconds() < (60 * 20):
            status = f"{computer_name} might be in use."
        else:
            status = f"{computer_name} is in use."
    else:
        status = f"{computer_name} is not in use."

    # Calculate time difference and format time_status
    if time_last_0_received:
        time_diff = (time_now - time_last_0_received).total_seconds()
    elif time_last_1_received:
        time_diff = (time_now - time_last_1_received).total_seconds()
    else:
        time_diff = 0

    formatted_time = format_time(time_diff)
    time_status = f"Last used: {formatted_time} ago"

    # Return both status and time_status
    return status, time_status


# Main script
# if __name__ == "__main__":
#     # Connecting to the SQLite database
#     connection = sqlite3.connect("..\\html_and_layout_data\\computer_status.db")
#     cursor = connection.cursor()

#     # Fetching specific columns from the database
#     cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM test_database")
#     rows = cursor.fetchall()

#     # Process data
#     for row in rows:
#         status, time_status = computer_status_update(row[0], row[1], row[2])
#         # Do something with status and time_status (e.g., print or store them)

#     # Closing database connection
#     connection.close()
