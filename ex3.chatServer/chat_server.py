"""EX  server_chat implementation
   Author: Raz Abergel 313575185
   Date:21/11/22
   Possible client commands defined in chat_protocol.py
"""
from datetime import datetime
import socket
from random import random

import select
import chat_protocol

MAX_MSG_LENGTH = 1024

SERVER_IP = '0.0.0.0'


# NAME <name> will set name. Server will reply error if
# duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client


def create_server_rsp(cmd, client_names, socket_to_handle):
    cmd_list = cmd.split()

    # todo case sen is not good here
    """create a message for the client according to the command he sent"""
    Data_not_sen_case = cmd  # in order to get also small letters and not just capital
    if Data_not_sen_case[0:4] == "NAME":
        if socket_to_handle in client_names.keys():
            client_names[socket_to_handle] = cmd[4:]
            return "hello" + cmd[5:], None

    elif Data_not_sen_case == "GET_NAMES":
        return "Server sent" + client_names.values(), None

    elif Data_not_sen_case[0:3] == "MSG":
        if cmd_list[1] in client_names.values:
            len_of_first_two_words = len(cmd_list[0]) + len(cmd_list[1]) + 1
            client_dest_name = str(cmd_list[1])
            msg_to_send = Data_not_sen_case[len_of_first_two_words:]
            return "Server sent" + str(client_names[socket_to_handle]) + "sent" + msg_to_send, client_dest_name
        else:
            return "client name doesnt exist"
    elif Data_not_sen_case == "EXIT":
        return "goodbye", None
    else:
        return "not valid input,try again", None


# def check_cmd(data):
#     """Check if the command is defined in the protocol (e.g. NUMBER, HELLO, TIME, EXIT)"""
#     Data_not_sen_case = data.upper()  # in order to get also small letters and not just capital
#     if Data_not_sen_case == "NUMBER" or Data_not_sen_case == "HELLO" \
#             or Data_not_sen_case == "TIME" or Data_not_sen_case == "EXIT":
#         return True
#     else:
#         return False


def return_key(val, socket_names):
    """the func return the desired key given certain value"""
    for key, value in socket_names.items():
        if value == val:
            return key


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, chat_protocol.PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []
    clients_names = {}
    client_des_name = None

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [], 0.1)
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                clients_names[connection] = None
                client_sockets.append(connection)
                #print_client_sockets(client_sockets)
            else:
                valid_msg, cmd = chat_protocol.get_msg(current_socket)
                if valid_msg:
                    if cmd == "":
                        print("Connection closed", )
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        print_client_sockets(client_sockets)
                    else:
                        response, client_des_name = create_server_rsp(cmd, clients_names, current_socket)
                        if client_des_name is not None:
                            key_socket = return_key(client_des_name, clients_names)
                            messages_to_send.append((key_socket, response))
                        else:
                            messages_to_send.append((current_socket, response))

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                set_msg = chat_protocol.create_msg(data)
                current_socket.send(data.encode())
                messages_to_send.remove(message)


if __name__ == "__main__":
    main()
