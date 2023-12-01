
# This is our client.
# What it needs to do is run when the computer turns on, turns off,
# and enters and exits sleep mode. Very simple This is our client.
import socket
import os
if __name__ == '__main__':
    print("Hello World")
    s=socket.socket()
    #host=socket.gethostname() #server hostname
    host="127.0.0.1"
    port=12345 #same as server
    s.connect((host,port))
    content = "I am a computer"
    s.send(content.encode())
