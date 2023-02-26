# ex5.httpServer
# Ex 4.4 and 4.9 (in the book) - HTTP Server Shell
# Author: Raz abergel

# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose


import os
import socket

MSG_LENGTH = 1024
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.1

DEFAULT_URL = "C:\\NETWORKS\\works\\httpServer\\webroot\\index.html"
# Response options:
OK200_RESPONSE = "HTTP/1.1 200 OK\r\n"
MOVED302_RESPONSE = "HTTP/1.1 302 Moved Temporarily\r\n"  # moved response - URL redirection
NOT_FOUND404_RESPONSE = "HTTP/1.1 404 NOT FOUND\r\n"

# the dict redirect the old address to the new one
REDIRECTION_DICTIONARY = {'C:\\NETWORKS\\works\\httpServer\\webroot\\/index.bla': DEFAULT_URL}


def calc_triangle_area(para_url, client_socket):
    """The function calc the area of a triangle.
    it will extract the params from the data that client sent,check if
    the input is valid ( just positive numbers (int or float))
    and send the answer to the client
    """
    answer_length = ""
    two_param = para_url[1].split('&')  # index 0 = height , index 1 = width
    height = two_param[0][7:]
    width = two_param[1][6:]
    if height == '0' or width == '0':  # in case one of the boxes is empty
        answer = ": You must insert numbers on each box to get the result"
        answer_length = 'Content-length: {size}\r\n'.format(size=len(answer))
        client_socket.send((OK200_RESPONSE + answer_length + '\r\n' + answer).encode())
        return
    try:
        if float(height) and float(width):  # check if the height and width  contain only numbers ( int or float )
            # ,otherwise handle the exception.
            if height[0] != '-' and width[0] != '-':  # the calc will be without negative numbers
                area = str((float(height) * float(width)) / 2)
                answer_length = 'Content-length: {size}\r\n'.format(size=len(area))
                client_socket.send((OK200_RESPONSE + answer_length + '\r\n' + area).encode())
            else:
                client_socket.send((OK200_RESPONSE + answer_length
                                    + '\r\n' ": The parameters cannot be negative").encode())
    except Exception as e:  # if the params contain also non-numbers chars ,
        # the exception will catch this and send message to the client and the server.
        print("Error: {}".format(e))
        print("the client enter invalid input ,he should try again with numbers")
        client_socket.send((OK200_RESPONSE + answer_length
                            + '\r\n' + ": Invalid input ,try again with numbers").encode())


def get_file_data(filename):
    """The function get the url and return the data from the right path"""
    filename.replace(r'/', "\\")  # convert the web path '/' to windows path "\"
    file_handle = open(filename, "rb")  # read bytes because some information
    # is passed in bytes (like images for example)
    response_data = file_handle.read()
    file_handle.close()
    return response_data


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    http_header = ""  # contain all the headers
    get_parameters_resource = resource.split("?")  # split the url in case of calc area 4.9

    # add code that given a resource (URL and parameters) generates the proper response
    if resource == '/' or resource == "":  # the client-request is general url
        url = DEFAULT_URL
    else:  # chaining the url to the path
        url = "C:\\NETWORKS\\works\\httpServer\\webroot\\" + resource

    # check if URL had been redirected(302),valid(200),not found(404)
    if url in REDIRECTION_DICTIONARY:  # 302
        http_header = MOVED302_RESPONSE
        url = REDIRECTION_DICTIONARY[url]
    elif os.path.isfile(url):  # 200
        http_header = OK200_RESPONSE
    elif get_parameters_resource[0] == '/calculate-area':  # in case of calc area 4.9
        calc_triangle_area(get_parameters_resource, client_socket)
        return None
    else:  # 404
        client_socket.send(NOT_FOUND404_RESPONSE.encode())
        return None

    data = get_file_data(url)  # read the data from the webroot

    http_header += 'Content-length: {size}\r\n'.format(size=len(data))  # content-length header

    filetype = url.split(".")[-1]  # extract the file type of the clients request (comes after the coma)
    #  extract requested file type from URL (html, jpg etc)
    if filetype == 'html' or filetype == 'txt':
        http_header += "{}".format('Content-Type: text/html charset=utf-8\r\n')
    elif filetype == 'jpg':
        http_header += "{}".format('Content-Type: image/jpeg\r\n')
    elif filetype == 'ico':  # favicon
        http_header += "{}".format('Content-Type: image/ico\r\n')
    elif filetype == 'js':
        http_header += "{}".format('Content-Type: text/javascript charset=UTF-8\r\n')
    elif filetype == 'css':
        http_header += "{}".format('Content-Type: text/css\r\n')

    # read the data from the file
    http_header += '\r\n'  # the limits between the headers to the data
    http_response = http_header.encode() + data
    client_socket.send(http_response)


def validate_http_request(request):
    # """
    # Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    # """
    lines = request.split("\n")
    # Get the first line of the request, which should contain the request method, resource path, and HTTP version
    first_line = lines[0]
    # Split the first line into three parts: method, path, and version
    parts = first_line.split(" ")
    if len(parts) != 3:
        # The first line must contain exactly three parts: method, path, and version
        return False, None
    method, path, version = parts
    # Check if the method is one of the allowed HTTP methods
    if method not in ["GET"]:
        # the full http method list include more options "POST", "HEAD", "OPTIONS" etc...
        return False, None
    # Check if the path is a valid resource path
    if not path.startswith("/"):
        return False, None
    # Check if the version is a valid HTTP version
    if not version.startswith("HTTP/1."):
        return False
    # If all checks pass, return True and the url
    return True, path


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')

    while True:
        try:  # this exception meant to avoid the crash of the server when the socket time-out is over
            client_request = client_socket.recv(MSG_LENGTH).decode()  # read the request from the client
        except socket.error as e:
            print("Error: {}".format(e))
            continue

        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break

    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print("Listening for connections on port {}".format(PORT))

    while True:
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()
