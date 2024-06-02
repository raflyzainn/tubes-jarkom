import socket
import threading

HOST = '127.0.0.1'  
PORT = 8080         

def make_request(path):
    try:
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

            print(f"Response for {path}:\n{response.decode('utf-8')}\n")
    except Exception as e:
        print(f"Error making request to {path}: {e}")

def main():
    paths = []
    for i in range(3):
        path = input(f"Enter path of HTML file {i+1}: ")
        paths.append(path)

    threads = []
    for path in paths:
        thread = threading.Thread(target=make_request, args=(path,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
