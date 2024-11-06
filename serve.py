#!/bin/env python
import os
import socket
import sys
import signal

# -- SETUP CONFIG -- #
try:
    import config
    pconfig = config.get_config()
except:
    print("Failed to get config.py. Please put config.py in the same dir!")
    sys.exit(1)

# -- END CONFIG SETUP -- #

class AccessRestrictedError(Exception):
    """Exception raised for access-restricted files."""
    def __init__(self, message="Access to this file is restricted."):
        self.message = message
        super().__init__(self.message)

class FileNotFoundError(Exception):
    """Exception raised for file not found."""
    def __init__(self, message="Requested file didn't exist."):
        self.message = message
        super().__init__(self.message)

def handle_sigint(sig, frame, socket_inp):
    socket_inp.close()
    sys.exit()

def get_script_path() -> str:
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def html_ok(file_path:str, send_socket):
    content_type = 'Content-Type: text/html\r\n'
    # if 'favicon.ico' in file_path:
    #     content_type = 'Content-Type: image/x-icon\r\n'
    f = None
    if file_path.startswith('/'):
        file_path = convert_to_web_path(file_path[1:])

    if file_path.endswith('/'):
        file_path += 'index.html'

    for keyword in pconfig.private_file:
        if convert_to_web_path(keyword) == file_path:
            raise AccessRestrictedError()

    try:
        f = open(file_path)
        outputdata = f.read()
        f.close()
        
        send_socket.send("HTTP/1.1 200 OK\r\n".encode())
        send_socket.send(content_type.encode())
        send_socket.send("\r\n".encode())
        send_socket.send(outputdata.encode())
    except FileNotFoundError as e:
        raise e

def convert_to_web_path(path:str):
    if path.startswith("/"):
        path = path[1:]
    sc_path = get_script_path()
    full_path = sc_path + "/" + pconfig.web_path + "/" + path
    return full_path

def read_with_web_context(path) -> str:
    file_path = convert_to_web_path(path)
    with open(file_path) as f:
        content = f.read()
    return content

if __name__ == '__main__':
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    signal.signal(signal.SIGINT, lambda signum, frame: handle_sigint(signum, frame, serverSocket))

    serverSocket.bind(('', pconfig.port))
    serverSocket.listen(1)

    print(f"Server is running on port {pconfig.port}...")

    while True:
        connectionSocket, addr = serverSocket.accept()
        
        try:
            message = connectionSocket.recv(1024).decode()
            if len(message.split()) > 1:
                try:
                    html_ok(message.split()[1], connectionSocket)
                except FileNotFoundError:
                    content = read_with_web_context(pconfig.fof_html)
                    connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n".encode())
                    connectionSocket.send("\r\n".encode())
                    connectionSocket.send(content.encode())
                except AccessRestrictedError:
                    content = read_with_web_context(pconfig.fot_html)
                    connectionSocket.send("HTTP/1.1 403 Forbidden\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n".encode())
                    connectionSocket.send("\r\n".encode())
                    connectionSocket.send(content.encode())

        except Exception as e:
            print("An unexpected error occurred:", e)
            content = read_with_web_context(pconfig.fof_html)
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
            connectionSocket.send("Content-Type: text/html\r\n".encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.send(content.encode())
        
        finally:
            connectionSocket.close()

