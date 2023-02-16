import socket
# server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("e.e.0.0", 8821))

(client_name, client_address) = server_socket.recvfrom(1024)
data = client_name.decode()

response = "Hello " + data

server_socket. sendto(response.encode(), client_address)
server_socket.close()

#client
import socket

my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.sendto( 'Omer' .encode(), ("127.0.0.1", 8821))
(data, remote_address) = my_socket.recvfrom(1024)

print(' The server sent: ' + data.decode())
my_socket.close()
