import socket
import os

HOST = '127.0.0.1'  
PORT = 8080         

def handle_request(client_connection):
    request = client_connection.recv(1024).decode('utf-8')
    print(f"Request:\n{request}")

    lines = request.split("\r\n")
    if len(lines) > 0:
        request_line = lines[0]
        method, path, _ = request_line.split(" ")

        if path == '/':
            path = '/index.html'  

        
        file_path = '.' + path  
        try:
            with open(file_path, 'rb') as file:
                response_body = file.read()
            response_line = "HTTP/1.1 200 OK\r\n"
        except FileNotFoundError:
            response_line = "HTTP/1.1 404 Not Found\r\n"
            response_body = b"<h1>404 Not Found</h1>"

        response_headers = "Content-Length: {}\r\n\r\n".format(len(response_body))
        response = response_line.encode('utf-8') + response_headers.encode('utf-8') + response_body

        client_connection.sendall(response)

    client_connection.close()

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(1)
        print(f"Serving HTTP on {HOST} port {PORT} ...")

        while True:
            client_connection, client_address = server_socket.accept()
            handle_request(client_connection)

if __name__ == "__main__":
    start_server()
