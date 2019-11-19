# Establish network connection to houston/remote.py
# Acts as TCP/IP server

import socket
import logging

# Set a function to receive data from Houston and sends the return
def listen_unsafe(operation, port, keep_alive):
    host = '' # All network interfaces
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Quick unbind
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(1024) # Buffer size
                if not data: break

                response = operation(data.decode('utf-8'))
                conn.sendall(bytes(response, 'utf-8'))

                # Optionally loop until CLOSE-CONNECTION is sent or received
                if not keep_alive or data == b'CC' or response == 'CC':
                    logging.debug("Closing listener on port: " + port)
                    s.close()
                    return response

# TODO: Probably shouldn't do this
# Tends to throw tons of errors when closing, usually safe to ignore
def listen(operation, port, keep_alive=False):
    logging.debug("Listening on port: {}, keep_alive: {}".format(str(port), keep_alive))
    try:
        listen_unsafe(operation, port, keep_alive)
    except:
        logging.error("Networking error")

# Testing
def echo(data):
    return data

if __name__ == "__main__":
    print(listen(echo, 6969))