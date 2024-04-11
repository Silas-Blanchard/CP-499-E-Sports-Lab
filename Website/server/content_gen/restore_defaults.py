#Restores default values to the csv files.
import shutil
import os

from admin_page_datafill import get_paths

def get_default_paths():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    wanted_files = ["Book1.csv", "Walls.csv", "Decor.csv", "Manual_Booking.csv", "admin_page.html", "default_admin_page.txt", "labels.csv"]
    default_versions = [os.path.join(BASE_DIR, "..","html_and_layout_data","defaults",i) for i in wanted_files]
    to_be_replaced = [os.path.join(BASE_DIR, "..","html_and_layout_data",i) for i in wanted_files]
    return default_versions, to_be_replaced
def main():
    defaults, replaced = get_default_paths()
    for defa, repl in zip(defaults, replaced):
        shutil.copyfile(defa, repl)

if __name__ == "__main__":
    main()