import os
import csv
import sys

def get_paths(BASE_DIR):
    return(
        os.path.join(BASE_DIR, "..","html_and_layout_data","Book1.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Walls.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Decor.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","Manual Booking.csv"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","admin_page.html"),
        os.path.join(BASE_DIR, "..","html_and_layout_data","default_admin_page.txt")
    )

def update_HTML():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    computer_layout, wall_layout, decor_layout, bookings, admin_html_path, default_admin_path = get_paths(BASE_DIR)

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
    if(decor == ""):
        decor = "NONE"

    for row in book_reader:
        books+=str(row)
        books+="\n"
    if(books == ""):
        books = "NONE"
    
    #this bit takes the default html, which is a text file and can be manipulated with minimal imports
    #It adds the content of each csv file to it and then will save it to an HTML file which we treat like a text file
    #The "..." are a strange sequence someone won't likely use and also doesn't interact with HTML
    with open(default_admin_path, "r") as file:
        raw_html = str(file.read())
        raw_html = raw_html.replace("...1...",computers)
        raw_html = raw_html.replace("...2...",walls)
        raw_html = raw_html.replace("...3...",decor)
        raw_html = raw_html.replace("...4...",books)
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