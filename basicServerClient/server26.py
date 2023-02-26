"""EX 2.6 server implementation
    Author: Raz Abergel
   Date:6/11/22
   Possible client commands defined in protocol.py
"""
from datetime import datetime

import protocol
import socket
import random


CLEAN_SOCKET_SIZE = 1024


def create_server_rsp(cmd):
    """create a message for the client according to the command he sent"""
    Data_not_sen_case = cmd.upper()  # in order to get also small letters and not just capital
    if Data_not_sen_case == "NUMBER":
        return str(random.randint(0, 99))
    elif Data_not_sen_case == "HELLO":
        return "Raz's Server"
    elif Data_not_sen_case == "TIME":
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M:%S")
    elif Data_not_sen_case == "EXIT":
        return "goodbye"
    else:
        return ""


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g. NUMBER, HELLO, TIME, EXIT)"""
    Data_not_sen_case = data.upper()  # in order to get also small letters and not just capital
    if Data_not_sen_case == "NUMBER" or Data_not_sen_case == "HELLO" \
            or Data_not_sen_case == "TIME" or Data_not_sen_case == "EXIT":
        return True
    else:
        return False


def main():
    # Create TCP/IP socket object

    # Bind server socket to IP and Port

    # Listen to incoming connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()

    print("Server is up and running")
    # Create client socket for incoming connection
    (client_socket, client_address) = server_socket.accept()

    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print("the client sent " + cmd)
            # 2. Check if the command is valid, use "check_cmd" function
            if check_cmd(cmd):
                # 3. If valid command - create response
                response_to_client = create_server_rsp(cmd)
                message = protocol.create_msg(response_to_client)
                client_socket.send(message.encode())
                if cmd.upper() == "EXIT":  # If EXIT command, break from loop
                    break
            else:
                response = "invalid input,try again"
                message = protocol.create_msg(response)
                client_socket.send(message.encode())

        else:
            response = "Wrong protocol"
            message = protocol.create_msg(response)
            client_socket.send(message.encode())
            client_socket.recv(CLEAN_SOCKET_SIZE)  # Attempt to empty the socket from possible garbage

    print("Closing\n")
    # Close sockets
    client_socket.close()
    server_socket.close()


if __name__ == "__main__":
    main()
