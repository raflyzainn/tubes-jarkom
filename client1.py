import socket

HOST = '127.0.0.1'  
PORT = 8080         

def make_request(path):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        request_line = f"GET {path} HTTP/1.1\r\n"
        headers = "Host: {}\r\n\r\n".format(HOST)
        request = request_line + headers

        client_socket.sendall(request.encode('utf-8'))

        response = b""
        while True:
            chunk = client_socket.recv(1024)
            if not chunk:
                break
            response += chunk

        print(response.decode('utf-8'))

if __name__ == "__main__":
    path = input("Enter the path of the file to request (e.g., /index.html): ")
    make_request(path)
