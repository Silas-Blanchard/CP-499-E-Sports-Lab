Python 3.11.0 (main, Oct 24 2022, 18:26:48) [MSC v.1933 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> # This is our client.
... # What it needs to do is run when the computer turns on, turns off,
... # and enters and exits sleep mode. Very simple This is our client.
... import socket
... import os
... 
... if __name__ == '__main__':
...     s = socket.socket()
...     host = "10.16.30.199"
...     port = 12345  # same as server
...     # if the server is not on, it will be disruptive for the code to stay running
...     s.settimeout(2)
... 
...     s.connect((host, port))
...     content = os.getlogin() + " 0"
