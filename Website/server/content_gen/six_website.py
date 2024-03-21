import sqlite3
import csv
import os
from ComputerStatusUpdater import computer_status_update
from datetime import datetime, timedelta

def do_GET():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #print(os.listdir(os.path.join(BASE_DIR, "../html_and_layout_data" )))
    db_path, rect_csv_path, wall_csv_path, HTML_path = get_file_paths(BASE_DIR)

    # Database operations
    rows = fetch_database_data(db_path)

    # Read CSV files
    computers, walls = read_csv_files(rect_csv_path, wall_csv_path)

    # Generate HTML content with calendar events
    HTML_text = generate_html_content(rows, computers, walls)

    # Write HTML to file
    write_html_file(HTML_path, HTML_text)


def get_file_paths(BASE_DIR):
    return (
        os.path.join(BASE_DIR, ".." , "html_and_layout_data" , "computer_status.db"),
        os.path.join(BASE_DIR, ".." , "html_and_layout_data", "Book1.csv"),
        os.path.join(BASE_DIR, "..", "html_and_layout_data", "Walls.csv"),
        os.path.join(BASE_DIR, "..", "html_and_layout_data", "webber.html"),
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
    
    # Add the responsive iframe container
    HTML_text += """
    <div class="iframe-container">
        <iframe class="responsive-iframe" src="https://calendar.google.com/calendar/embed?height=600&wkst=1&bgcolor=%23ffffff&ctz=America%2FDenver&showTitle=0&showCalendars=0&src=Y2Nlc3BvcnRzQGNvbG9yYWRvY29sbGVnZS5lZHU&color=%23D81B60" frameborder="0" scrolling="no"></iframe>
    </div>
    """
    
    # Continue with the SVG content
    HTML_text += "<svg viewBox='0 0 1000 1000'>"
    
    # Add computers and walls to SVG
    HTML_text += generate_computers_svg(rows, computers)
    HTML_text += generate_walls_svg(walls)
    HTML_text += generate_computers_list_svg(rows, computers, 1000)  # Adjust the width as needed

    # Add pop-up HTML
    HTML_text += """
    <div id="welcomePopupModal" class="welcome-popup">
        <div class="welcome-popup-content">
            <span class="welcome-popup-close">&times;</span>
            <p>Welcome to the Esports Lab Viewer! This is a resource to see what computers are currently open or in-use. Please be mindful of practice times and closed lab events!</p>
            <p>Looking to be a part of the Colorado College Esports community? Be sure to join the 
            <a href="https://discord.com/invite/Ker2VQa" target="_blank">Discord!</a> 
            </p>
            <p>Interested in getting card access to the lab? Be sure to join the Discord and reach out to Josh (JoamL) to learn about gaining access!</p>
        </div>
    </div>
    """
    
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
        /* alignment-baseline: middle; */
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
        color: #333333;
    }

    .events-container {
        display: flex;
        justify-content: space-between; /* Space out the children evenly */
        align-items: flex-start; /* Align children at their top edge */
        padding: 10px;
        background: #444; /* A different shade for contrast */
        color: white;
        margin: 0 auto; /* Center the container */
        max-width: calc(100% - 20px); /* Adjust the width to not exceed the parent's width considering padding */
    }

    .events-column {
        flex-basis: calc(50% - 20px); /* Subtract the padding from the width */
        text-align: center; /* Center text within each column */
        padding: 0 10px; /* Add some padding on the left and right */
    }

    /* Ensure the list takes up full width of the column */
    #events-list-today, #events-list-tomorrow {
        list-style-type: none;
        padding: 0;
        margin: 0;
        width: 100%;
    }

    #events-list-today li, #events-list-tomorrow li {
        margin: 5px 0; /* Margin for list items */
    }

    .welcome-popup {
        display: none; /* Hidden by default */
        position: fixed; /* Stay in place */
        z-index: 10; /* Sit on top */
        left: 0;
        top: 0;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    }

    .welcome-popup-content {
        background-color: #D09B2C; /* Matching the header's background color */
        margin: 10% auto; /* 10% from the top and centered */
        padding: 20px;
        border: 1px solid #222; /* Black border for emphasis */
        width: 50%; /* Width can be adjusted for different screen sizes */
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        text-align: center; /* Center the text */
        color: #000; /* Text color */
        font-family: 'Arial', sans-serif; /* Assuming Arial is used on the website */
    }

    .welcome-popup-close {
        color: #aaa;
        float: right;
        font-size: 28px;
        font-weight: bold;
        cursor: pointer;
    }

    .welcome-popup-close:hover,
    .welcome-popup-close:focus {
        color: #000; /* Change color on hover/focus for better visibility */
        text-decoration: none;
    }

    .iframe-container {
        position: relative;
        overflow: hidden;
        width: 100%; /* full width */
        padding-top: 56.25%; /* aspect ratio */
    }

    .responsive-iframe {
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        right: 0;
        width: 100%;
        height: 100%;
        border: none;
    }
    </style>
    """
    return styles


def generate_header():
    # Header for website with logo on the left, title centered, and login button on the right
    header="""
    <div class="header">
        <div class="logo-container">
            <img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/ff/Colorado_College_Tigers_logo.svg/800px-Colorado_College_Tigers_logo.svg.png" alt="CC Logo" class="logo" />
        </div>
        <h1 class="header-title">CC Esports Lab</h1>
        <a href="https://cas.coloradocollege.edu/cas/login?service=http://esportscomm.coloradocollege.edu/login/cas" class="login-button" class="login-button">Login</a>
    </div>
    """
    # http://localhost:3001/  ||  http://esportscomm.coloradocollege.edu/
    # admin for admin page
    # Combine the two headers
    return header

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
    box_color = "#801B1B"  # default to red
    if "is not in use" in status:
        box_color = "#228C22"
    elif "might be in use" in status:
        box_color = "#D09B2C"

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
            computer_name_csv_text = computer_name_csv + "_text"

            # Update the status message presentation here
            list_content += f"""
            <text id="{computer_name_csv_text}" x="{list_x}" y="{list_y_start + index * line_height}" fill="black">
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
          
          let text_name = computer
          let text_id = text_name.concat("_text")//simply the name of the text bits we have
          if(dataJSON[computer] == "#801B1B"){
            let computer_stat = computer.concat(": In Use");
            document.getElementById(text_id).innerHTML = computer_stat
          }else if(dataJSON[computer] == "#D09B2C"){
            let computer_stat = computer.concat(": Likely In Use");
            document.getElementById(text_id).innerHTML = computer_stat
          }else{
            let computer_stat = computer.concat(": Free");
            document.getElementById(text_id).innerHTML = computer_stat
          }
        }
      });
      // Get the modal
      var modal = document.getElementById('welcomePopupModal');

      // Get the <span> element that closes the modal
      var span = document.getElementsByClassName('welcome-popup-close')[0];

      // When the page loads, open the modal 
      window.onload = function() {
          modal.style.display = 'block';
      }

      // When the user clicks on <span> (x), close the modal
      span.onclick = function() {
          modal.style.display = 'none';
      }

      // When the user clicks anywhere outside of the modal, close it
      window.onclick = function(event) {
          if (event.target == modal) {
              modal.style.display = 'none';
          }
      }
    </script>
    """
    with open(HTML_path, "w") as file:
        file.write(HTML_text)
        file.close()


# Main execution block
do_GET()
