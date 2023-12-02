# first of all import the socket library
import socket

def find_computer_status(name, status):
    if status == 0:
        result_status = name + ' is in use'
    elif status == 1:
        result_status = name + ' might be in use'
    else:
        raise Exception("Invalid computer status")

    return result_status


if __name__ == '__main__':
    # next create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")

    # reserve a port on your computer in our
    # case it is 12345, but it can be anything
    port = 12345

    # Next bind to the port
    s.bind(('', port))
    print("socket bound to %s" % port)

    # put the socket into listening mode
    s.listen(20)
    print("socket is listening")

    # a forever loop until we interrupt it or
    # an error occurs
    clients = []
    while True:
        # Establish connection with client and store it for later
        c, addr = s.accept()
        print('Got connection from', addr)
        clients.append(addr)

        # create a variable to hold the message the computer sent
        message = (c.recv(1024).decode())

        #closing the connection after information is received
        c.close()

        # split the message into 2 parts
        message_split = message.splitlines(' ')

        # get the name
        computer_name = message_split[0]

        # get the status number
        computer_status = int(message_split[1])

        # Print to make sure we split correctly
        print("Computer Name:", computer_name)
        print("Computer Status:", computer_status)
