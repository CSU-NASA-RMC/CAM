# Establish network connection to houston/remote.py
# Acts as TCP/IP server

import socket

# Set a function to receive data from Houston and sends the return
# Input and output are byte objects
def listen(operation, port):
    host = '' # All network interfaces

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024) # Buffer size
                if not data: break
                response = operation(data)
                conn.sendall(response)
                return response
    return