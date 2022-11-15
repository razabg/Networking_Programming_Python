"""EX 2.6 client implementation
   Author: Raz Abergel 313575185
   Date:6/11/22
   Possible client commands defined in protocol.py
"""

import socket
import protocol

MAX_LENGTH_OF_MESSAGE = 99


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    # 1. Add length field ("HELLO" -> "04HELLO")
    # 2. Send it to the server
    # 3. Get server's response
    # 4. If server's response is valid, print it
    # 5. If command is EXIT, break from while loop

    # Possible client commands: not case-sensitive!
    # NUMBER - server should reply with a random number, 0-99
    # HELLO - server should reply with the server's name, anything you want
    # TIME - server should reply with time and date
    # EXIT - server should send acknowledge and quit
    while True:
        user_input = input("Enter command:\n")
        if len(user_input) > MAX_LENGTH_OF_MESSAGE:  # to avoid the user send illegal input that won't be according
            # to the protocol
            print("the input is too long, try again")
            continue
        message = protocol.create_msg(user_input)
        my_socket.send(message.encode())
        valid_msg, cmd = protocol.get_msg(my_socket)
        if valid_msg:
            print(cmd)
            if cmd == "goodbye":
                break
        else:
            print("wrong protocol\n")

    print("Closing\n")
    # Close socket
    my_socket.close()


if __name__ == "__main__":
    main()
