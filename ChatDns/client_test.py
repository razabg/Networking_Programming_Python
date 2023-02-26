# "python C:\NETWORKS\works\chatServer\chat_client.py"

"""EX  client_chat implementation
   Author: Raz Abergel
   Date:21/11/22
   Possible client commands defined in chat_protocol.py
"""


import socket
import msvcrt
import select

MAX_LENGTH_OF_MESSAGE = 99
HOME_IP = "127.0.0.1"
BACKSPACE = '\x08'
ENTER = '\r'


# NAME <name> will set name. Server will reply error if
# duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect((HOME_IP, 5555))

    user_input = ""
    print("pls enter commands:\n")
    while True:
        rlist, wlist, xlist = select.select([my_socket], [my_socket], [], 0.1)
        if len(rlist) != 0:  # unlike the server, there is no need to iterate over the list because
            # we know that we have only one element in the list = my_socket
            #valid_msg, cmd = chat_protocol.get_msg(rlist[0])
            data = rlist[0].recv(1024).decode()
            if len(data) != 0:
                if data == "EXIT":
                    break
                print()
                print(data + "\n")

            else:  # we will get here only of there is a disruption with length field of the protocol
                print("wrong protocol\n")

        if len(wlist) != 0:  # unlike the server, there is no need to iterate over a list because
            # we know that we have only one element in the list = my_socket
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch.isascii():  # the program will work only with ascii characters
                    ch = ch.decode()
                    print(ch, end="", flush=True)
                    if ch == BACKSPACE:  # delete the last character
                        user_input = user_input[:-1]
                        continue
                    if ch == ENTER:
                        if user_input == '':  # cover the case that the user press enter and the user input is still
                            # empty
                            print("pls enter commands:\n")
                            continue

                        if len(user_input) > MAX_LENGTH_OF_MESSAGE:  # in case the input is too long
                            print()
                            print("The message is too long,try again\n")
                            user_input = ""
                            continue
                        wlist[0].send(user_input.encode())
                        user_input = ""  # erase the user input
                        print()
                    else:
                        user_input += ch

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()