"""EX  TEST A 2023
   Author: Raz Abergel 313575185
   Date:17/2/23
"""
from scapy.all import *
import socket
import select



MAX_MSG_LENGTH = 1024
SERVER_IP = '0.0.0.0'
IP_PATTERN = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$" # regex ip pattern




def dns_request_type_a(url):
    """Regular mapping (A), url name -> ip"""
    dns_query = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(qname=url)
    result = sr1(dns_query, timeout=1)
    counter = result[DNS].ancount  # counter of the query's answers
    ip_list = ""
    if counter == 0:
        data = "Error! the website is not exists ,try again"
        return data
    if counter == 1:
        ip_list += result[DNSRR][0].rdata + "\n"
        return ip_list

    for i in range(0, counter):  # loop over the ans' and take the rdata section
        if is_valid_ipv4(str(result[DNSRR][i].rdata)):  # check if the rdata contains ipv4
            ip_list += result[DNSRR][i].rdata + "\n"

    return ip_list



# NAME <name> will set name. Server will reply error if
# duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client
def create_server_rsp(cmd, client_names, socket_to_handle,clients_ip_dic,client_address):
    """The function create the proper response to a certain client according to the message that the client has sent.
    The func get the following parameters: input = cmd , the dict of the clients = client_names,the dict that holds ip of every name clients_ip_dic,the tuple of the client_address
    the socket we handle  = socket_to_handle """

    cmd_list = cmd.split()  # the split of the message into a list help to manage and sent the right response

    if cmd_list[0] == "NSLOOKUP" and len(cmd_list) == 2:
        if cmd_list[1] in client_names.values(): # if the ip address is belong to one of the clients or to a website
            answer = str(return_key(cmd_list[1],clients_ip_dic)[0]) #return the key of the value with the desired name
            return answer, None
        else:
            answer = dns_request_type_a(cmd_list[1])
            return answer ,None


    if cmd_list[0] == "NAME" and len(cmd_list) != 1:
        if len(cmd_list) > 2:  # if the name has more than one word,it's illegal
            return "Server Sent: The name should have just one word! try again", None
        if not cmd_list[1].isalpha():
            return "The name must consist of only letters ", None

        if socket_to_handle in client_names.keys():
            if cmd_list[1] not in client_names.values():
                client_names[socket_to_handle] = cmd_list[1]  # adding the name to the dict right to its socket key
                if client_address in clients_ip_dic.keys():
                    if  cmd_list[1] not in clients_ip_dic.values():
                        clients_ip_dic[client_address] = cmd_list[1] # add the name of the client as value to its address
                return "Server Sent: Hello " + cmd_list[1], None
            else:
                return "Server Sent: Name already exists,try different name", None

    elif cmd == "GET_NAMES":
        name_list = ""
        for name in client_names.values():
            if name is not None:
                name_list += str(name) + " "  # chaining the names of the clients
        return "Server sent: " + name_list, None

    elif cmd_list[0] == "MSG" and len(cmd_list) != 1:
        if client_names[socket_to_handle] is None:  # The client must have name if he wants to send messages
            return "You must have name before you send message", None
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


def is_valid_ipv4(ip):
    """Check if the given ip is valid (using regex)"""
    return bool(re.match(IP_PATTERN, ip))
def return_key(val, socket_names):
    """The func return the desired key given certain value"""
    for key, value in socket_names.items():
        if value == val:
            return key


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, 5555))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []
    clients_names = {}  # dictionary that holds the client sockets and their names
    clients_ip_dic = {}  # dictionary that holds the clients names and their ip addresses
    client_des_name = None  # we will store here the name of the dest socket
    client_address = ""

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [], 0.1)
        for current_socket in rlist:  # iterate on the readable list to see if there is a
            # client that the server needs to read from him message
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                clients_ip_dic[client_address] = None # create dic that the keys are the client addresses
                clients_names[connection] = None
                client_sockets.append(connection)
            else:  # if it's a client socket, and we want the read the message that he sent
                try:
                    #valid_msg, cmd = chat_protocol.get_msg(current_socket)
                    data_from_client = current_socket.recv(1024).decode()
                    if len(data_from_client) == 0:
                        #if cmd == "":
                        print("Connection closed", )
                        client_sockets.remove(current_socket)
                        current_socket.close()
                    else:
                            response, client_des_name = create_server_rsp(data_from_client, clients_names, current_socket,clients_ip_dic,client_address)

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
                    #set_msg = chat_protocol.create_msg(data)
                    current_socket.send(data.encode())
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
