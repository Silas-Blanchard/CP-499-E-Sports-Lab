import sqlite3
import csv
import os
from ComputerStatusUpdater import computer_status_update

# Custom request handler class
def do_GET():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path, rect_csv_path, wall_csv_path, HTML_path = get_file_paths(BASE_DIR)

    # Database operations
    rows = fetch_database_data(db_path)

    # Read CSV files
    computers, walls = read_csv_files(rect_csv_path, wall_csv_path)

    # Generate HTML content
    HTML_text = generate_html_content(rows, computers, walls)

    # Write HTML to file
    write_html_file(HTML_path, HTML_text)


def get_file_paths(BASE_DIR):
    return (
        os.path.join(BASE_DIR, "computer_status.db"),
        os.path.join(BASE_DIR, "Book1.csv"),
        os.path.join(BASE_DIR, "Walls.csv"),
        os.path.join(BASE_DIR, "webber.html"),
    )


def fetch_database_data(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name, time_last_0_received, time_last_1_received FROM computer_status")
    rows = cursor.fetchall()
    connection.close()
    return rows


def read_csv_files(rect_csv_path, wall_csv_path):
    with open(rect_csv_path, "r") as file:
        computers = list(csv.reader(file, delimiter=','))
        computers = computers[1:]  # Skip header row

    with open(wall_csv_path, "r") as file:
        walls = list(csv.reader(file, delimiter=','))
        walls = walls[1:]  # Skip header row
    
    return computers, walls


def generate_html_content(rows, computers, walls):
    # Start HTML content generation (including styles and headers)
    HTML_text = "<html><head><title>Esports Lab</title></head><body>"
    HTML_text += generate_styles()
    HTML_text += generate_header()
    HTML_text += "<svg viewBox='0 0 1000 1000'>"
    
    # Add computers and walls to SVG
    HTML_text += generate_computers_svg(rows, computers)
    HTML_text += generate_walls_svg(walls)
    HTML_text += generate_computers_list_svg(rows, computers, 1000)  # Adjust the width as needed

    # Close SVG and add remaining HTML content
    HTML_text += "</svg></body></html>"
    return HTML_text


def generate_styles():
    #Style section
    styles="""
        <style>

        svg {
            background-color: #333333; /* Dark grey background */
        }

        rect {
            fill: #4CAF50; /* Green color for computer rectangles */
        }

        .wall {
            fill: #555555; /* Lighter grey for walls */
        }

        text {
            fill: white;
            font-size: 14px;
        }
        
        .computer-text {
            /* Styles for text inside the rectangles */
            font-size: 14px; /* Adjust to fit inside the rectangles */
            dominant-baseline: middle;
            text-anchor: middle;
            pointer-events: none; /* Ensures the text doesn't interfere with rectangle clicks */
        }

        .header {
            padding: 10px 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #D09B2C;
            color: black;
        }

        g:hover > text {
            display: block;
        }

        g:focus > text {
            display: block;
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

        .events-header {
            background: #444; /* A different shade for contrast */
            color: white;
            padding: 5px 20px 20px 20px; /* Increased bottom padding */
            text-align: center;
        }

        #events-list {
            margin: 0;
            font-size: 14px;
        }

    </style>"""
    return styles


def generate_header():
    # Header for website with logo on the left, title centered, and login button on the right
    header="""
    <div class="header">
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/ff/Colorado_College_Tigers_logo.svg/800px-Colorado_College_Tigers_logo.svg.png" alt="CC Logo" class="logo" />
        </div>
        <h1 class="header-title">CC Esports Lab</h1>
        <button class="login-button">Login</button>
    </div>
    """

      # Additional header for displaying the events of the day
    events_header = """
    <div class="events-header">
        <h2>Today's Practices</h2>
        <p id="events-list">No events scheduled for today.</p>
    </div>
    """

    # Combine the two headers
    return header + events_header


def get_identifier(computer_name):
    if 'VarsityLab' in computer_name:
        return computer_name.replace('VarsityLab', '')
    if 'EventSpace' in computer_name:
        return 'E' + computer_name.replace('EventSpace', '')
    return ''  # Default case if none of the above matches


def generate_computers_svg(database_rows, computers_csv):
    svg_content = ""
    for computer in computers_csv:
        computer_name_csv = computer[0] 
        # Find the matching row from the database
        matching_row = next((row for row in database_rows if row[0] == computer_name_csv), None)

        if matching_row:
            # Extract the identifier number or letter from the computer name
            identifier = get_identifier(computer_name_csv)
            # Call the function to generate SVG for this computer
            svg_content += generate_computer_svg(matching_row, computer, identifier)

    return svg_content


def generate_computer_svg(row, computer, identifier):
    computer_name = row[0]
    time_last_0_received = row[1]
    time_last_1_received = row[2]
    status, _ = computer_status_update(computer_name, time_last_0_received, time_last_1_received)

    # Determine the box color based on status
    box_color = "red"  # default to red
    if "is not in use" in status:
        box_color = "dark green"
    elif "might be in use" in status:
        box_color = "yellow"

    # Extract position and size from the CSV
    x, y = int(computer[1]), int(computer[2])
    width, height = 35, 35  # example size

    # Create SVG group for the computer
    svg_computer = f"""
        <g>
            <rect id="{computer_name}" x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{box_color};"/>
            <text class="computer-text" x="{x + width/2}" y="{y + height/2}" fill="white">{identifier}</text>
        </g>
        """
    return svg_computer


def generate_computers_list_svg(database_rows, computers_csv, svg_width):
    list_content = "<g>"
    list_x = svg_width - 200  # Assume this places the list to the right
    list_y_start = 10  # Align with the top of the walls
    line_height = 18.8

    for index, computer in enumerate(computers_csv, start=1):
        computer_name_csv = computer[0]
        matching_row = next((row for row in database_rows if row[0] == computer_name_csv), None)

        if matching_row:
            status, _ = computer_status_update(matching_row[0], matching_row[1], matching_row[2])

            # Update the status message presentation here
            list_content += f"""
            <text x="{list_x}" y="{list_y_start + index * line_height}" fill="black">
                {computer_name_csv}: {('In Use' if 'is in use' in status else 'Free')}
            </text>
            """

    list_content += "</g>"
    return list_content


def generate_walls_svg(walls):
    # Generate SVG for walls
    svg_content = ""
    for wall in walls:
        svg_content += generate_wall_svg(wall)
    return svg_content


def generate_wall_svg(wall):
    x, y = int(wall[1]), int(wall[2])
    if wall[4] == "TRUE":
        width = int(wall[3])
        height = 5
    else:
        width = 5
        height = int(wall[3])

    # Create SVG rectangle for the wall
    svg_content = f"""<rect class="wall" x="{x}" y="{y}" width="{width}" height="{height}"></rect>"""
    return svg_content


def write_html_file(HTML_path, HTML_text):
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
    with open(HTML_path, "w") as file:
        file.write(HTML_text)


# Main execution block
do_GET()
