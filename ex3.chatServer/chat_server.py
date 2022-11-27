"""EX  server_chat implementation
   Author: Raz Abergel 313575185
   Date:21/11/22
   Possible client commands defined in chat_protocol.py
"""

import socket
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
    """The function create the proper response to a certain client according to the message that the client has sent.
    The func get the following parameters: input = cmd , the dict of the clients = client_names,
    the socket we handle  = socket_to_handle """

    cmd_list = cmd.split()  # the split of the message into a list help to manage and sent the right response

    if cmd_list[0] == "NAME":
        if len(cmd_list) > 2:  # if the name has more than one word,it's not legal
            return "Server Sent: The name should have just one word! try again", None
        if not cmd_list[1].isalpha():
            return "The name must consist of only letters ", None

        if socket_to_handle in client_names.keys():
            if cmd_list[1] not in client_names.values():
                client_names[socket_to_handle] = cmd_list[1]  # adding the name to the dict right to its socket key
                return "Server Sent: Hello " + cmd_list[1], None
            else:
                return "Server Sent: Name already exists,try different name", None

    elif cmd == "GET_NAMES":
        name_list = ""
        for name in client_names.values():
            if name is not None:
                name_list += str(name)  # chaining the names of the clients
                name_list += " "
        return "Server sent: " + name_list, None

    elif cmd_list[0] == "MSG":
        if cmd_list[1] in client_names.values():
            len_of_first_two_words = len(cmd_list[0]) + len(cmd_list[1]) + 1  # the length of the first two words
            # MSG + name of the client
            client_dest_name = str(cmd_list[1])
            msg_to_send = cmd[len_of_first_two_words:]  # the content of the message will come after the input of the
            # command and the client's name
            return "Server sent: " + str(client_names[socket_to_handle]) + " sent" + msg_to_send, client_dest_name
        else:
            return "Client name doesn't exist", None
    elif cmd == "EXIT":
        client_names.pop(socket_to_handle)  # pop the client out of the dict
        return "EXIT", None
    else:  # in case of every other input
        return "Not valid input,try again", None


def close_client_connection(current_socket, clients_names):
    """The function close the connection with client in case that the client suddenly closed"""
    clients_names.pop(current_socket)
    current_socket.close()


def return_key(val, socket_names):
    """The func return the desired key given certain value"""
    for key, value in socket_names.items():
        if value == val:
            return key


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, chat_protocol.PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []
    clients_names = {}  # dictionary that holds the client sockets and their names
    client_des_name = None  # we will store here the name of the dest socket
    client_address = ""

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [], 0.1)
        for current_socket in rlist:  # iterate on the readable list to see if there is a
            # client that the server needs to read from him message
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                clients_names[connection] = None
                client_sockets.append(connection)
            else:  # if its client socket and we want the read the message that he sent
                try:
                    valid_msg, cmd = chat_protocol.get_msg(current_socket)
                    if valid_msg:
                        if cmd == "":
                            print("Connection closed", )
                            client_sockets.remove(current_socket)
                            current_socket.close()
                        else:
                            response, client_des_name = create_server_rsp(cmd, clients_names, current_socket)
                            if client_des_name is not None:  # if the client want to send a message to someone else
                                key_socket = return_key(client_des_name, clients_names)
                                messages_to_send.append((key_socket, response))
                            else:
                                messages_to_send.append((current_socket, response))
                except Exception as e:  # the purpose of the exception is to avoid the crash of server if we force
                    # closing of one of the clients
                    print("Error: {}".format(e))
                    print("The connection with current client has lost", client_address)
                    close_client_connection(current_socket, clients_names)
                    client_sockets.remove(current_socket)
                    continue

        for message in messages_to_send:
            current_socket, data = message
            if current_socket in wlist:
                try:
                    set_msg = chat_protocol.create_msg(data)
                    current_socket.send(set_msg.encode())
                    messages_to_send.remove(message)
                except Exception as e:  # the purpose of the exception is to avoid the crash of server if we force
                    # closing of one of the clients
                    print("Error: {}".format(e))
                    print("The connection with current client has lost", client_address)
                    close_client_connection(current_socket, clients_names)
                    client_sockets.remove(current_socket)
                    continue


if __name__ == "__main__":
    main()
