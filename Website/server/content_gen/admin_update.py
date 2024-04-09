import os
import csv
import sys
from admin_page_datafill import get_paths

def split_input(txt):

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    computer_path, wall_path, decor_path, booking_path, admin_html_path, default_admin_path, box_path = get_paths(BASE_DIR)
    computers = []
    bookings = []
    walls = []
    decor = []
    texts = []
    #super simple just splits up the input and has each piece replace the targetted files.
    for element in txt.split("\n"):
        if len(element.split()) > 0:
            if element.split(";")[1] == "selectable computer": #accessing HTML element class and this is where it will always be
                attributes = element.split(";")
                computers.append([attributes[0], attributes[3], attributes[4]]) #this is all that goes into the computer location csv
                bookings.append(attributes[2].split(","))
            if element.split(";")[1] == "selectable wall": 
                attributes = element.split(";")
                del attributes[1]
                walls.append(attributes[:5]) #this is all that goes into the computer location csv
            if element.split(";")[1] == "selectable decor": 
                attributes = element.split(";")
                del attributes[1]
                decor.append(attributes[:5]) #this is all that goes into the computer location csv
            if element.split(";")[1] == "selectable decortext": 
                attributes = element.split(";")
                del attributes[1]
                texts.append(attributes[:-1]) #this is all that goes into the computer location csv

    update_computers(computers, computer_path)
    update_walls(walls, wall_path)
    update_decor(decor, decor_path)
    update_booking(bookings, booking_path)
    update_text(texts, box_path)

#updates the Book1.csv
def update_computers(txt, file):
    with open(file, 'w', newline='') as f:
        writr = csv.writer(f)
        writr.writerow(["Name","X","Y"])
        [writr.writerows(txt)] #txt is a list of lists
  
#updating each of the csv files
def update_walls(txt, file):
    with open(file, 'w', newline='') as f:
        writr = csv.writer(f)
        writr.writerow(["Walls","X","Y","Length","Rotate"])
        [writr.writerows(txt)] #txt is a list of lists

def update_decor(txt, file):
    with open(file, 'w', newline='') as f:
        writr = csv.writer(f)
        writr.writerow(["Name","x","y","width","height"])
        [writr.writerows(txt)] #txt is a list of lists

def update_booking(txt,file):
   with open(file, 'w', newline='') as f:
        writr = csv.writer(f)
        writr.writerow(["Name","Status"])
        [writr.writerows(txt)] #txt is a list of lists

def update_text(txt, file):
     with open(file, 'w', newline='') as f:
        writr = csv.writer(f)
        writr.writerow(["Label","x","y","size"])
        [writr.writerows(txt)] #txt is a list of lists

# def update_notices(txt, file):
#     #TODO
#     pass

def main():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    unparsed_path = os.path.join(BASE_DIR, "..","html_and_layout_data","unparsed.txt")

    split_input(open(unparsed_path).read())

if __name__ == "__main__":
    main()
