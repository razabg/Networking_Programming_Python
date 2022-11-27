import msvcrt

def close_client_connection(current_socket,clients_names):
    clients_names.pop(socket)
    current_socket.close()
# try:
# except Exception as e:
#     print("Error: {}".format(e))
#     close_client_connection(current_socket, clients_names)
#     client_sockets.remove(current_socket)
#     continue
def main():
    # create a dictionary
    my_dict = {
        "name": "John",
        "city": "New York",
        "profession": "Engineer"
    }

    # check if a value - Engineer exists in the values list
    if "Engineer" in my_dict.values():
        print("Value exists in the dictionary")
    else:
        print("Value does not exist in the dictionary")
    # user_input = ""
    # while True:
    #     if msvcrt.kbhit():
    #         ch = msvcrt.getch().decode()
    #         print(ch, end="", flush=True)
    #         if ch == '\r':
    #             print(user_input)
    #             user_input = ""
    #            # wlist[0].send(chat_protocol.create_msg(user_input).encode())
    #         else:
    #             user_input += ch

    # user_input = "not come "
    # while True:
    #     if msvcrt.kbhit():
    #         ch = msvcrt.getch().decode()
    #         print(ch, flush=True)
    #         if ch == '\r':
    #             print(user_input)
    #             break
    #         else:
    #             user_input += ch

    # num = 0
    # while num < 10:
    #     if msvcrt.kbhit():
    #         user_input = msvcrt.getch()
    #         num += 1
    #         print(user_input.decode(), flush=True)
    # print(num, end="", flush=True)


if __name__ == "__main__":
    main()

# while True:
#     if msvcrt.kbhit():
#         key_stroke = msvcrt.getch()
#         if key_stroke == b'\x1b':
#             print("Esc key pressed")
#         else:
#             print(str(key_stroke).split("'")[1], "key pressed")
