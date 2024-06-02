import socket
import sys

def send_http_request(server_host, server_port, filename):
    # Membuat socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        # Menghubungkan ke server
        client_socket.connect((server_host, server_port))
        
        # Membuat permintaan HTTP
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\nConnection: close\r\n\r\n"
        
        # Mengirimkan permintaan ke server
        client_socket.sendall(request.encode())

        # Menerima respons dari server
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data
        
        # Menampilkan respons dari server
        print(response.decode())

if __name__ == "__main__":
    # Menerima argumen baris perintah
    if len(sys.argv) != 4:
        print("Format: client.py server_host server_port filename")
        sys.exit(1)
    
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Mengirimkan permintaan HTTP
    send_http_request(server_host, server_port, filename)
