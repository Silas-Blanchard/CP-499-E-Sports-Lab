import sqlite3
from ComputerStatusUpdater import computer_status_update
import csv
import os


# Custom request handler class
def do_GET():
    # Connecting to the SQLite database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "test_database.db")
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    #leading this program in no uncertain terms to the correct files
    rect_csv_path = os.path.join(BASE_DIR, "Book1.csv")
    wall_csv_path = os.path.join(BASE_DIR, "Walls.csv")
    HTML_path = os.path.join(BASE_DIR, "webber.html")

    # Fetching specific columns from the database
    cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM test_database")
    rows = cursor.fetchall()

    # Constructing HTML response with database data
    HTML_text = """<html><head><title>SQLite Data</title></head>"""
    HTML_text += "<body><p>Database Content:</p><ul>"

    #Style section
    HTML_text +="""
    <style>
        text{
            display: none;
            fill:#fff;
            font-size:12;
        }

        g:hover > text {
            display: block;
        }
        .rectangle {
            width: 40px;
            height: 20px;
        }

        .rotatedrectangle{
            transform: rotate(90)
        }

        .container {{
            display: grid;
            grid-template_rows: 50px 50px 50px 50px 50px 50px 50px 50px 50px 50px;
            grid-template-columns: 50px ;

        }}
    </style>
    """
    # reading computers CSV
    file_in = open(rect_csv_path, "r")
    csv_readr = csv.reader(file_in, delimiter=',')
    readr = list(csv_readr)

    counter = 0
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
        if csv_line[3] == "TRUE":
            the_class = "rectangle rotatedrectangle"
        else:
            the_class = "rectangle"

        counter += 1

        new_line= f"""
<g>
    <div id={computer_name} class="{the_class}" style="background-color:{box_color};">\n
        <title>Computer Name: {computer_name}, Status: {status}, Time Status: {time_status}</title>
    </div>
    <text>Computer Name: {computer_name}, Status: {status}, Time Status: {time_status}</text>
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
            new_line = f"""<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:white;"/>"""
            HTML_text = "% s\n %s" % (HTML_text, new_line)

    # closing out HTML file
    HTML_text = "% s\n %s" % (HTML_text, "</svg>")
    HTML_text += """</ul>
    <script src="/socket.io/socket.io.js"></script>
    <script>
      const socket = io();
    </script></body></html>
"""
    
    f = open(HTML_path, "w")
    f.write(HTML_text)
    f.close()

    # Closing database connection
    connection.close()


# Main execution block
do_GET()
