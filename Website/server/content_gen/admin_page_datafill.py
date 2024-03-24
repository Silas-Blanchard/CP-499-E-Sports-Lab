import os
import csv
import sys

def get_paths(BASE_DIR):
    return(
        os.path.join(BASE_DIR, "..","html_and_layout_data","Book1.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Walls.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Decor.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Manual_Booking.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","admin_page.html"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","default_admin_page.txt"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","labels.csv")
    )

def update_HTML():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    computer_layout, wall_layout, decor_layout, bookings, admin_html_path, default_admin_path, labels = get_paths(BASE_DIR)

    computer_reader = csv.reader(open(computer_layout), delimiter=",")
    wall_reader = csv.reader(open(wall_layout), delimiter=",")
    decor_reader = csv.reader(open(decor_layout), delimiter=",")
    book_reader = csv.reader(open(bookings), delimiter=",")
    label_reader = csv.reader(open(labels), delimiter=",")

    computers = walls = decor = books = ""

    HTML = """
    <svg viewBox='-10 0 1000 500'>
    """
    
    #Takes everything from the computer layout CSV and makes it into its HTML representation
    for row, status in zip(list(computer_reader)[1:], list(book_reader)[1:]):
        computer_name, x, y = row
        is_in_order = status[1]
        data_id = computer_name + "," + is_in_order
        HTML+= f"""
            <rect id = "{computer_name}" class="selectable computer" data-id="{data_id}" x="{x}" y="{y}" width="35" height="35"/>
        """

    #This takes everything from the wall layout CSV and makes it into HTML
    for row in list(wall_reader)[1:]:
        x, y = int(row[1]), int(row[2])
        name = row[0]
        #determines orientation
        if row[4] == "TRUE":
            width = int(row[3])
            height = 5
        else:
            width = 5
            height = int(row[3])
        
        HTML += f"""
        <rect id = "{name}" class="wall selectable" x="{x}" y="{y}" width="{width}" height="{height}"></rect>
        """

    #takes everythign in decor.csv and makes it into HTML
    for row in list(decor_reader)[1:]:
        decor, x, y, width, height, label = row
        HTML += f"""
        <rect id="{decor}" class="selectable decor" x="{x}" y="{y}" width="{width}" height="{height}" style="fill:#808080;"></rect>
        """

    #Displays booked computers
    for count, row in enumerate(list(book_reader)[1:]):
        computer, status = row
        x = 750
        y = 10 + 50*count
        HTML += f"""<g>
        <rect class="selectable" x="{x}" y="{y}" width="200" height="40" style="fill:#808080;"></rect>
        <text class="computer-text" x="{x+10}" y="{y + 25}" fill="white">{computer}: {status}</text>
        </g>
        """
    
    for row in list(label_reader)[1:]:
        text, x, y, size = row
        HTML += f"""
            <text id="{text}" class="selectable decortext" x="{x}" y="{y}" data-id="{text}">{text}</text>
        """
    
    #this bit takes the default html, which is a text file and can be manipulated with minimal imports
    #It adds the content of each csv file to it and then will save it to an HTML file which we treat like a text file
    #The "..." are a strange sequence someone won't likely use and also doesn't interact with HTML
    with open(default_admin_path, "r") as file:
        raw_html = str(file.read())
        raw_html = raw_html.replace("...0...",HTML)
        with open(admin_html_path, "w") as file:
            file.write(raw_html)
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