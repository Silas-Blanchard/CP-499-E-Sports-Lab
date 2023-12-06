from http.server import BaseHTTPRequestHandler, HTTPServer
import sqlite3
from ComputerStatusUpdater import computer_status_update
import csv

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
        HTML_text = "<html><head><title>SQLite Data</title></head>"
        HTML_text += "<body><p>Database Content:</p><ul>"

        #reading CSV
        file_in = open("Book1.csv", "r")
        csv_readr = csv.reader(file_in, delimiter=',')
        readr = list(csv_readr)

        countr = 0

        #initial svg section of our HTML document
        HTML_text += """<svg viewBox="0 0 1000 1000">"""
            
        #Loop
        for row in rows:
            #variables that define the parameters of our rectangle
            computer_name = row[0]
            time_last_0_received = row[1]
            time_last_1_received = row[2]
            status, time_status = computer_status_update(computer_name, time_last_0_received, time_last_1_received)
            
            #which color we are using
            if "is not in use" in status:
                box_color = "red"
            elif "might be in use" in status:
                box_color = "yellow"
            else:
                box_color = "green"

            #CSV varibles
            csv_line = readr[countr + 1]
            x = int(csv_line[1])
            y = int(csv_line[2])
            if(csv_line[3] == "TRUE"):
                height = 40
                width = 20
            else:
                height = 20
                width = 40

            countr+=1
            #Example: <rect x="120" y="120" width="100" height="100"/>            
            new_line = f"""<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{box_color};"/>"""
            HTML_text = "% s\n %s" % (HTML_text, new_line)

        #closing out HTML file
        HTML_text = "% s\n %s" % (HTML_text,"</svg>")
        HTML_text += "</ul></body></html>"

        print(HTML_text)

        # Send the HTML response to the client
        self.wfile.write(bytes(HTML_text, "utf-8"))

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
