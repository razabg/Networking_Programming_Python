import msvcrt


def main():
    user_input = "not come "
    while True:
        if msvcrt.kbhit():
            ch = msvcrt.getch().decode()
            print(ch, end="", flush=True)
            if ch == '\r':
                print(user_input)
                break
            else:
                user_input += ch

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
