# This is our client.
# What it needs to do is run when the computer turns on, turns off,
# and enters and exits sleep mode. Very simple This is our client.
import socket
import os

if __name__ == '__main__':
    s = socket.socket()
    host = "172.22.32.52"
    port = 12345  # same as server
    # if the server is not on, it will be disruptive for the code to stay running
    s.settimeout(2)

    s.connect((host, port))
    content = os.getlogin() + ' 2'

    s.send(content.encode())
