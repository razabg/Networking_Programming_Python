"""EX protocol implementation for chat
   Author: Raz Abergel
   Date:21/11/22

"""

LENGTH_FIELD_SIZE = 2
PORT = 8820


def create_msg(data):
    """Create a valid protocol message, with length field"""
    length_data = str(len(data))
    z_fil_len = length_data.zfill(LENGTH_FIELD_SIZE)
    message = z_fil_len + data
    return message


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length_of_the_message = (my_socket.recv(LENGTH_FIELD_SIZE).decode())
    if length_of_the_message.isdigit():
        data = my_socket.recv(int(length_of_the_message)).decode()
        return True, data
    else:
        return False, "Error"


