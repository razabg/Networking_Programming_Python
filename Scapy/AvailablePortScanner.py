
import socket

target = "127.0.0.1"  # Replace with the IP address or hostname of the target machine
port_range = range(1, 1025)  # Scan all ports from 1 to 1024

for port in port_range:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)  # Set a timeout of 100 milliseconds
    try:
        s.connect((target, port))
    except Exception as e:
        print(f"Port {port} is closed")
    else:
        print(f"Port {port} is open")
        s.close()
