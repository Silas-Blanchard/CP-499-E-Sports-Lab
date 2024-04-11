This repository is the capstone project for Silas Blanchard and Quinn Sebso—two seniors at Colorado College. Our program aims to address a fundamental problem with the Colorado College esports lab; there is no way to know how busy the lab is without being there. For many students, particularly in cold months, the walk to the lab could be a huge wasted effort if they find it to be full. Our project is a website, built using node js, that displays which computers are in use and which are free. Available to anyone on the Colorado College campus (and using a Colorado College network), this project is currently deployed and visitable at http://esportscomm.coloradocollege.edu

If you are on campus, visit today (we are proud of our work and want people to see it)

The project has three main parts: the website, the server, and the lab computers.

Installation and operation procedures can be found here:
https://docs.google.com/document/d/1Gbk26AQQR50lvck4qG3Cwwc0CK82GKBLDHK_NAvysS0

Modify port numbers in the files under /PYW Files to suit your needs. The default port is 12345 for our server, which is under Website/server

The project is currently maintained by @Silas-Blanchard and @qsebso on github
Contact us at silasb3435@gmail.com or q_sebso@coloradocollege.edu respectively

File Structure:
/CP-499-E-Sports-Lab/
>PYW Files—Files to be downloaded on the esports lab machines.
>Website—The bulk of the project. Within it is the web hosting and server code. Additionally, the database and settings are stored in this folder. We run "npm start" in this level (see operation procedures above)
>XML Files—Non-code that stores Windows Task Scheduler settings for easy installation.
The other files in the top directory are files created by node.js

/CP-499-E-Sports-Lab/Website:
>Server: Most project code is kept here. Contains index.js and server with database.py, the most important parts of the project
>node_modules: used for node.js to specify certain attributes of the project

/CP-499-E-Sports-Lab/Website/server:
>content-gen: Contains files that produce the files in html_and_layout_data
>html_and_layout_data: Contains files as well as default settings in the form of CSV files (also includes default versions of the HTML files)
>tests: Contains programs useful in bug-fixing. Remains in place in anticipation of future versions.
