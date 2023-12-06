import csv
import random

#the input file and the output file
def getColor():
    colors = ["maroon", "gold", "#060"]
    return random.choice(colors)

def placeRectangles(inputname, outputname):
    file_in = open(inputname, "r")
    page_out = open(outputname, 'w')

    readr = csv.reader(file_in, delimiter=',')
    first = True

    rect_elements = []
    #<rect x="120" y="120" width="100" height="100"/>

    #initial svg section of our HTML document
    HTML_text = """<svg viewBox="0 0 500 500">"""
        
    
    for line in readr:
        if(not first):
            x = int(line[1])
            y = int(line[2])
            color = getColor()
            if(line[3] == "TRUE"):
                height = 40
                width = 20
            else:
                height = 20
                width = 40
            new_line = f"""<rect x="{x}" y="{y}" width="{width}" height="{height}" style="fill:{color};"/>"""
            HTML_text = "% s\n %s" % (HTML_text, new_line)
        else:   
            first = False
    HTML_text = "% s\n %s" % (HTML_text,"</svg>")
    return(HTML_text)

print(placeRectangles("Book1.csv","page1.html"))

    
    
