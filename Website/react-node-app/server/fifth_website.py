import sqlite3
from ComputerStatusUpdater import computer_status_update
import csv
import os


# Custom request handler class
def do_GET():
    # Connecting to the SQLite database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "computer_status.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    #leading this program in no uncertain terms to the correct files
    rect_csv_path = os.path.join(BASE_DIR, "Book1.csv")
    wall_csv_path = os.path.join(BASE_DIR, "Walls.csv")
    HTML_path = os.path.join(BASE_DIR, "webber.html")

    # Fetching specific columns from the database
    cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM computer_status")
    rows = cursor.fetchall()

    # Constructing HTML response with database data
    HTML_text = """<html><head><title>Esports Lab</title></head>"""
    HTML_text += "<body><ul>"

    #Style section
    HTML_text +="""
        <style>
            text {
                display: none;
                fill: #000000;
                font-size: 12;
            }

            g:hover > text {
                display: block;
            }

            g:focus > text {
                display: block;
            }

            .header {
                padding: 10px 5px; /* First value is for top and bottom, second is for left and right */
                display: flex;
                justify-content: space-between;
                align-items: center;
                background: #1abc9c;
                color: white;
            }

            .logo-container {
                padding-left: 20px; /* Adjust as needed */
            }

            .logo {
                height: 80px; /* Adjust the size as needed */
            }

            .header-title {
                flex-grow: 1;
                text-align: center;
                margin: 0; /* This ensures the title is truly centered */
            }

            .login-button {
                margin-right: 20px; /* Adjust as needed */
                background: #f2f2f2;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                cursor: pointer;
                border-radius: 5px;
            }
        </style>
        """

    # Header for website with logo on the left, title centered, and login button on the right
    HTML_text += """
    <div class="header">
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/ff/Colorado_College_Tigers_logo.svg/800px-Colorado_College_Tigers_logo.svg.png" alt="CC Logo" class="logo" />
        </div>
        <h1 class="header-title">CC Esports Lab</h1>
        <button class="login-button">Login</button>
    </div>
    """
    
    # reading computers CSV
    file_in = open(rect_csv_path, "r")
    csv_readr = csv.reader(file_in, delimiter=',')
    readr = list(csv_readr)

    counter = 0

    # initial svg section of our HTML document
    HTML_text += """<svg viewBox="0 0 1000 1000">"""

    # Loop
    for row in rows:
        # variables that define the parameters of our rectangle
        computer_name = row[0]
        time_last_0_received = row[1]
        time_last_1_received = row[2]
        status, time_status = computer_status_update(computer_name, time_last_0_received, time_last_1_received)

        # which color we are using
        if "is not in use" in status:
            box_color = "green"
        elif "might be in use" in status:
            box_color = "yellow"
        else:
            box_color = "red"

        # CSV variables
        csv_line = readr[counter + 1]
        x = int(csv_line[1])
        y = int(csv_line[2])
        height = 35
        width = 35

        counter += 1

        # Example: <rect x="120" y="120" width="100" height="100"/>
        new_line = f"""
<g>
    <rect id="{computer_name}" x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{box_color};">\n
        <!<title>Computer Name: {computer_name}, Status: {status}, Time Status: {time_status}</title>-- -->
    </rect>
    <text x="0" y="400">Computer Name: {computer_name}, Status: {status}, Time Status: {time_status}</text>
</g>

"""

        HTML_text += new_line

    # reading CSV for walls
    file_in = open(wall_csv_path, "r")
    readr = csv.reader(file_in, delimiter=',')

    # wall loop
    for wall in readr:
        if wall[1] != "X":
            # CSV variables
            x = int(wall[1])
            y = int(wall[2])
            if wall[4] == "TRUE":
                height = 5
                width = int(wall[3])
            else:
                height = int(wall[3])
                width = 5

            counter += 1
            # Example: <rect x="120" y="120" width="100" height="100"/>
            new_line = f"""<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:black;"/>"""
            HTML_text = "% s\n %s" % (HTML_text, new_line)

    # closing out HTML file
    HTML_text = "% s\n %s" % (HTML_text, "</svg>")
    HTML_text += """</ul>    
    <script src="/socket.io/socket.io.js"></script>
    <script>
      const socket = io();
        
      socket.on('update', function (data) {
        const dataJSON = JSON.parse(data)
        console.log(dataJSON)
        for (var computer in dataJSON) {
          let svg = document.getElementById(computer);
          svg.style.fill = dataJSON[computer];
        }
      });
    </script></body></html>
    """
    
    f = open(HTML_path, "w")
    f.write(HTML_text)
    f.close()

    # Closing database connection
    connection.close()


# Main execution block
do_GET()
