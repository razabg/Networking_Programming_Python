# "C:\NETWORKS\works\ex3.chatServer\chat_client.py"

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


# NAME <name> will set name. Server will reply error if
# duplicate
# GET_NAMES will get all names
# MSG <NAME> <message> will send message to client name
# EXIT will close client

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", chat_protocol.PORT))
    messages_to_send = []

    user_input = ""
    print("pls enter commands:\n")
    while True:
        rlist, wlist, xlist = select.select([my_socket], [my_socket], [], 0.1)
        if msvcrt.kbhit():
            ch = msvcrt.getch().decode()
            print(ch, end="", flush=True)
            if ch == '\r':
                my_socket.send(chat_protocol.create_msg(user_input).encode())
            else:
                user_input += ch

        if rlist == my_socket:
            valid_msg, cmd = chat_protocol.get_msg(my_socket)
            if valid_msg:
                print(cmd)
                if cmd == "goodbye":
                    break
            else:
                print("wrong protocol\n")

            # else:

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
