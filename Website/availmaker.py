import codecs
import webbrowser
import time
import os

def get_data(name):
    return [os.getlogin(), str(time.time()), name]

if __name__ == '__main__':
    computer = "Varsity 1"
    #basic setup
    f = open('availpage.html', 'w')

    clients = ["Varsity 1", "Varsity 2", "Varsity 3"]
    data = [get_data(i) for i in clients]
    
    table = tabulate(table, tablefmt='html')

    html_template =f"""
    <html> 
    <head></head> 
    <body> 
    <p>{computer}</p>
    {table}
    </body>
    
    </html>""
    """
    
    f.write(html_template)

    f.close()

    #opening the file
    webbrowser.open('availpage.html')
