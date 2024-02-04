Use these commmands to run the program on linux! 
index.js and server with database.py are the cores of this project, one is for the website and the other is for the server.

sudo fuser -k 3001/tcp && sudo fuser -k 3000/tcp
npm start & python3 server\ with\ database.py

Alternative command:
nohup npm start > web_server_log.txt & nohup python3 server\ with\ database.py > comp_server_log.txt &
