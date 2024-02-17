import os
import csv
import sys

def get_paths(BASE_DIR):
    return(
        os.path.join(BASE_DIR, "..","html_and_layout_data","Book1.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Walls.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Decor.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Manual Booking.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","admin_page.html")
    )

def update_HTML():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    computer_layout, wall_layout, decor_layout, bookings, admin_html_path = get_paths(BASE_DIR)

    computer_reader = csv.reader(open(computer_layout), delimiter=",")
    wall_reader = csv.reader(open(wall_layout), delimiter=",")
    decor_reader = csv.reader(open(decor_layout), delimiter=",")
    book_reader = csv.reader(open(bookings), delimiter=",")

    computers = walls = decor = books = ""

    #this takes all the data and makes it into a tab delineated list that the HTML page will handle
    for row in computer_reader:
        computers+=str(row)
        computers+="\n"

    for row in wall_reader:
        walls+=str(row)
        walls+="\n"

    for row in decor_reader:
        decor+=str(row) 
        decor+= "\n"

    for row in book_reader:
        books+=str(row)
        books+="\n"

    json_content =f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Computer Availability</title>
    <style type="text/css">

    body{{
    background-color:linen;
    }}

    h1{{
    color:black;
    margin-left: 40px;
    }}

    .warning {{
        background-color: #D09B2C;
        padding: 10px;
        border-left: 5px solid red;
        margin: 20px 0;
        font-weight: bold;
    }}

    .header {{
        padding: 10px 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #D09B2C;
        color: white;
    }}

    .textbox{{
        height:200px;
        width:400px;
        font-size:14pt;
    }}

    .logo-container {{
        padding-left: 20px;
    }}

    .logo {{
        height: 80px;
    }}

    .header-title {{
        flex-grow: 1;
        text-align: center;
        margin: 0;
    }}

    .login-button {{
        margin-right: 20px;
        background: #f2f2f2;
        border: none;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        cursor: pointer;
        border-radius: 5px;
    }}

    .example-text {{
    color: #555; /* Darker text for examples */
    background-color: #f8f8f8; /* Light background for the example area */
    padding: 10px;
    border-left: 4px solid #999; /* A left border to highlight it's an example */
    font-family: monospace; /* Monospaced font for code-like examples */
    margin-bottom: 10px;
    }}

    .textarea{{
        width: 1000px
    }}
    </style>

    </head>
        <body>
            <div class="header">
                <div class="logo-container">
                    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/f/ff/Colorado_College_Tigers_logo.svg/800px-Colorado_College_Tigers_logo.svg.png" alt="CC Logo" class="logo" />
                </div>
                <h1 class="header-title">CC Esports Admin Page</h1>
            </div>
            <div class="warning">
                <h2>ADMINS ONLY</h2>
                <p>Changing these files will change the arrangement of the computers, walls, and decortations in the lab!</p>
                <ul>
                    <li>Computer Arrangement Syntax: Computer Name, X Position, Y Position</li>
                    <li>Wall Arrangement Syntax: Wall Name, Starting X, Starting Y, Length, Rotation (Enter TRUE or FALSE or it will break)</li>
                    <li>Decor Arrangement Syntax: Decor Name, Starting X, Starting Y, Width, Height</li>
                    <li>(0,0) meaning X = 0 and Y = 0 is the top left of the screen</li>
                </ul>
            </div>

            <form>
                <label for="comparr">Computer Arrangement CSV:</label><br>
                <p class="example-text">Example: VarsityLab1, 10, 200</p>
                <textarea class="textbox textarea" id="comparr">{computers}</textarea>
                <br>
                <button onclick="saveComputers()">Save</button>
                <button onclick="restoreComputers()">Restore Default</button> 
                <br>
                <label for="wallarr">Wall Arrangement CSV:</label><br>
                <p class="example-text">Example: NorthWall, 0, 0, 700, TRUE (FALSE makes the wall go horizantal TRUE makes it vertical)</p>
                <textarea class="textbox textarea" id="wallarr">{walls}</textarea>
                <br>
                <button onclick="saveWalls()">Save</button>
                <button onclick="restoreWalls()">Restore Default</button> 
                <br>
                <label for="decarr">Decor Arrangement CSV:</label><br>
                <p class="example-text">Example: "Switch, 50, 75, 20, 30"</p>
                <textarea class="textbox textarea" id="decarr">{decor}</textarea>
                <br>
                <button onclick="saveDecor()">Save</button>
                <button onclick="restoreBooking()">Restore Default</button>
                <br>
                <label for="bookarr">Availability CSV:</label><br>
                <p class="example-text">Example: "Close Time, Close Date, Open Time, Open Date"</p>
                <textarea class="textbox textarea" id="decarr">{books}</textarea>
                <br>
                <button onclick="saveBooking()">Save</button>
                <button onclick="restoreBooking()">Restore Default</button> 
            </form>
        </body>
        """
    json_content += """
        <script src="/socket.io/socket.io.js"></script>
            <script>
                const socket = io();
                function myFunciton() {
                    alert('Button clicked!');
                }
                function saveComputers(){
                    alert('Computers Saved')
                }
                function saveLayout(){
                    alert('Layout Saved')
                }
                function saveDecor(){
                    alert('Decor Saved')
                }
                function saveBooking(){
                    alert('Availability Saved')
                }

                function restoreComputers(){
                    alert('Computers Restored')
                }
                function restoreLayout(){
                    alert('Layout Restored')
                }
                function restoreDecor(){
                    alert('Decor Restored')
                }
                function restoreBooking(){
                    alert('Availability Restored')
                }
            </script>
        </html>"""

    with open(admin_html_path, "w") as file:
        file.write(json_content)
        file.close()

#Takes a string input and processes it to update files
def update_files(files):
    separate_files = files.split(";")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    computer_layout_path, wall_layout, decor_layout, bookings, admin_html_path = get_paths(BASE_DIR)

    with open(computer_layout_path, "w") as file:
        file.write(separate_files[0])
        file.close()

def restore_original():
    pass

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        update_HTML()
    elif(sys.argv[1] == "1"):
        update_files(sys.argv[2])