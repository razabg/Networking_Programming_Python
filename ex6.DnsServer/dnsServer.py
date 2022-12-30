# ex6.DnsServer over http-server (using scapy).
# implementing nslookup commands : A query and PTR query.
# Author: Raz abergel.


from scapy.layers.dns import DNSQR, DNS, DNSRR
from scapy.layers.inet import UDP, IP
from scapy.all import *
import socket
import re

MSG_LENGTH = 1024
IP_SOCKET = '0.0.0.0'
PORT = 8153
SOCKET_TIMEOUT = 0.1
OK200_RESPONSE = "HTTP/1.1 200 OK\r\n"
REV_POST = ".in-addr.arpa"
IP_PATTERN = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"


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
        ip_list += result[DNSRR][0].rdata + '<br>'
        return ip_list

    for i in range(0, counter):  # loop over the ans' and take the rdata section
        if is_valid_ipv4(str(result[DNSRR][i].rdata)):  # check if the rdata contains ipv4
            ip_list += result[DNSRR][i].rdata + '<br>'

    return ip_list


def dns_request_type_ptr(ip):
    """Reverse mapping (PTR), ip ->url name"""
    canonical_name = ""
    dns_query = IP(dst='8.8.8.8') / UDP(sport=24601, dport=53) / DNS(qdcount=1, rd=1) / DNSQR(
        qname=rev_ip(ip) + REV_POST, qtype='PTR')

    result = sr1(dns_query, timeout=1)
    if not result.haslayer(DNSRR):  # in case there is no canonical name
        canonical_name = "This IP has no canonical name"
        return canonical_name
    decoded_name = result[DNSRR][0].rdata.decode()
    canonical_name += decoded_name + '<br>'
    return canonical_name


def rev_ip(ip):
    """reverse the ip address for the ptr query"""
    reversed_ip = ".".join(reversed(ip.split(".")))
    return reversed_ip


def is_valid_ipv4(ip):
    """Check if the given ip is valid (using regex)"""
    return bool(re.match(IP_PATTERN, ip))


def handle_internet_crash(client_socket):
    """In case of network failure ,the function will be called and send message to the client"""
    http_header = OK200_RESPONSE
    data = "There is a problem with your internet , try to fix the problem"
    http_header += 'Content-length: {size}\r\n'.format(size=len(data))  # content-length header
    http_header += "{}".format('Content-Type: text/html charset=utf-8\r\n')
    http_header += '\r\n'  # the limits between the headers to the data
    http_response = http_header.encode() + str(data).encode()
    client_socket.send(http_response)


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    get_splited_resource = resource.split("/")
    data = ""
    http_header = ""  # contain all the headers
    http_header = OK200_RESPONSE

    if resource == '/' or resource == "":  # no request
        data = "Insert valid IP or URL"
    elif len(get_splited_resource) == 2:  # A type request
        try:
            data = dns_request_type_a(resource[1:])
        except Exception as e:  # in case of internet failure the server will still work
            print("Error: {}".format(e))
            handle_internet_crash(client_socket)
            return
    elif get_splited_resource[1] == "reverse" and is_valid_ipv4(get_splited_resource[2]):  # PTR type request
        try:
            data = dns_request_type_ptr(get_splited_resource[2])
        except Exception as e:  # in case of internet failure the server will still work
            print("Error: {}".format(e))
            handle_internet_crash(client_socket)
            return
    else:
        data = "Invalid input, check if your ip is valid and try again"

    if len(data) == 0:
        data = "Error! there is a problem with request ,try again"

    http_header += 'Content-length: {size}\r\n'.format(size=len(data))  # content-length header
    http_header += "{}".format('Content-Type: text/html charset=utf-8\r\n')
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
