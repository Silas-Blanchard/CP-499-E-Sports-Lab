
# This is our client.
# What it needs to do is run when the computer turns on, turns off,
# and enters and exits sleep mode. Very simple This is our client.

if __name__ == '__main__':
    print("Hello World")

import socket
import os
s=socket.socket()
#host=socket.gethostname() #server hostname
host="10.16.32.7"
port=12000 #same as server
s.connect((host,port))
content = "I am a computer"
s.send(content.encode())
