# ex6.DnsServer over http-server
# implementing nslookup command
# Author: Raz abergel 313575185
from scapy.layers.dns import DNSQR, DNS, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.sendrecv import sr1
from scapy.all import *
import os
import socket

MSG_LENGTH = 1024
IP_SOCKET = '0.0.0.0'
PORT = 8153
SOCKET_TIMEOUT = 0.1
OK200_RESPONSE = "HTTP/1.1 200 OK\r\n"


def dns_request_type_a(url):
    dns_query = IP(dst="8.8.8.8") / UDP(sport=24601, dport=53) / DNS(qdcount=1) / DNSQR(qname=url)
    result = sr1(dns_query)
    counter = result[DNS].ancount # counter of the query answers
    ip_list = ""
    for i in range(1, counter): # loop over the ans and take the rdata section
        ip_list += result[DNSRR][i].rdata + '<br>'

    return ip_list


def dns_request_type_ptr(ip):
    pass


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    http_header = ""  # contain all the headers
    http_header = OK200_RESPONSE
    if resource == '/' or resource == "":
        data = "insert valid ip or url"
    else:
        data = dns_request_type_a(resource[1:])
    if len(data) == 0:
        data = "Error! there is no such url or ip ,try again"

    # else:  # 404
    #     client_socket.send(NOT_FOUND404_RESPONSE.encode())
    #     return None

    http_header += 'Content-length: {size}\r\n'.format(size=len(data))  # content-length header
    http_header += "{}".format('Content-Type: text/html charset=utf-8\r\n')

    # read the data from the file
    http_header += '\r\n'  # the limits between the headers to the data
    http_response = http_header.encode() + str(data).encode()
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
    server_socket.bind((IP_SOCKET, PORT))
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
