# "python C:\NETWORKS\works\ex3.chatServer\chat_client.py"

"""EX  client_chat implementation
   Author: Raz Abergel 313575185
   Date:21/11/22
   Possible client commands defined in chat_protocol.py
"""

import socket
import chat_protocol
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
    my_socket.connect((HOME_IP, chat_protocol.PORT))
    messages_to_send = []

    user_input = ""
    print("pls enter commands:\n")
    while True:
        rlist, wlist, xlist = select.select([my_socket], [my_socket], [], 0.1)
        if len(rlist) != 0:  # unlike the server, there is no need to iterate over the list because
            # we know that we have only one element in the list = my_socket
            valid_msg, cmd = chat_protocol.get_msg(rlist[0])
            if valid_msg:
                if cmd == "EXIT":
                    break
                print()
                print(cmd + "\n")

            else:  # we will get here only of there is a disruption with length field of the protocol
                print("wrong protocol\n")

        if len(wlist) != 0:
            if msvcrt.kbhit():
                ch = msvcrt.getch()
                if ch.isascii():  # the program will work only with ascii characters
                    ch = ch.decode()
                    print(ch, end="", flush=True)
                    if ch == BACKSPACE:
                        user_input = user_input[:-1]
                        continue
                    if ch == ENTER:
                        if user_input == '':  # cover the case that the user press enter and send empty message
                            user_input = "not valid"

                        if len(user_input) > MAX_LENGTH_OF_MESSAGE:  # in case the input is too long
                            print()
                            print("The message is too long,try again\n")
                            user_input = ""
                            continue
                        wlist[0].send(chat_protocol.create_msg(user_input).encode())
                        user_input = ""  # clean the variable
                        print()
                    else:
                        user_input += ch

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
