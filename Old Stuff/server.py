
# first of all import the socket library
import socket
import subprocess

if __name__ == '__main__':
  # next create a socket object
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print ("Socket successfully created")

  # reserve a port on your computer in our
  # case it is 12345 but it can be anything
  port = 12345

  # Next bind to the port  
  s.bind(('', port))
  print ("socket binded to %s" %(port))

  # put the socket into listening mode
  s.listen(5)
  print ("socket is listening")

  # a forever loop until we interrupt it or
  # an error occurs
  clients = []
  while True:

  # Establish connection with client and store it for later
    c, addr = s.accept()
    print ('Got connection from', addr )
    clients.append(addr)
    
    # recieve what the client has to say
    print(c.recv(1024).decode())

    # Close the connection with the client since this is just a ping
    c.close()


