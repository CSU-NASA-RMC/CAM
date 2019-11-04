# Establish network connection to houston/remote.py
# Acts as TCP/IP client

import socket

def send(data):
    host = "127.0.0.1" # Can probably be done automatically
    port = 42069 # Houston port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(data)
        return s.recv(1024)

if __name__ == "__main__":
    print(send(b"CaN yOu HeaR mE?1?!"))