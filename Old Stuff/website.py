from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
from ComputerStatusUpdater import computer_status_update

# Define server details
hostName = "localhost"
serverPort = 8080


# Custom request handler class
class MyServer(BaseHTTPRequestHandler):
    # Handle GET requests
    def do_GET(self):
        # Send a 200 OK response with HTML content type
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Connecting to the SQLite database
        connection = sqlite3.connect('test_database.db')
        cursor = connection.cursor()

        # Fetching specific columns from the database
        cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM test_database")
        rows = cursor.fetchall()

        # Constructing HTML response with database data
        response = "<html><head><title>SQLite Data</title></head>"
        response += "<body><p>Database Content:</p><ul>"

        # Iterate through rows and create list items in HTML
        for row in rows:
            # Open a list item
            response += "<li>"

            # Add the content of each list item
            computer_name = row[0]
            time_last_0_received = row[1]
            time_last_1_received = row[2]
            status, time_status = computer_status_update(computer_name, time_last_0_received, time_last_1_received)

            response += "{} {}".format(status, time_status)

            # Determine the color based on the status
            if "is not in use" in status:
                box_color = "green"
            elif "might be in use" in status:
                box_color = "yellow"
            else:
                box_color = "red"

            # Add a box or container next to each list item with dynamic color
            response += "<div style='border: 1px solid #000; padding: 5px; display: inline-block; margin-left: 10px; " \
                        "background-color: {};'>".format(
                            box_color)
            response += "&nbsp;"  # Add a non-breaking space for better visibility
            response += "</div>"

            # Close the list item
            response += "</li>"

        response += "</ul></body></html>"

        # Send the HTML response to the client
        self.wfile.write(bytes(response, "utf-8"))

        # Closing database connection
        connection.close()


# Main execution block
if __name__ == "__main__":
    # Create an instance of the HTTPServer with the custom handler
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        # Start serving requests indefinitely
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to gracefully stop the server
        pass

    # Close the server when done
    webServer.server_close()
    print("Server stopped.")
