import socket
import os

# Menentukan alamat dan port server
serverHost = '127.0.0.16'
serverPort = 12345

def handle_client(client_connection):
    # Menerima permintaan dari klien dan mendekodekannya
    request = client_connection.recv(1024).decode('utf-8')

    # Menganalisis permintaan HTTP
    request_lines = request.split("\r\n")
    request_method, request_path, _ = request_lines[0].split(" ")

    # Mendapatkan path file yang diminta
    if request_path == '/':
        request_path = '/index.html'

    file_path = '.' + request_path

    # Membuat pesan respons HTTP
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response_body = file.read()
        response_status_line = "HTTP/1.1 200 OK\r\n"
        response_headers = f"Content-Type: text/html\r\nContent-Length: {len(response_body)}\r\n\r\n"
        response = response_status_line.encode('utf-8') + response_headers.encode('utf-8') + response_body
    else:
        response = b"HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>"

    # Mengirim respons ke klien
    client_connection.sendall(response)

    # Menutup koneksi dengan klien
    client_connection.close()

def start_server():
    # Membuat socket server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((serverHost, serverPort))
        server_socket.listen(1)
        print(f"Server berjalan di http://{serverHost}:{serverPort}")

        while True:
            # Menerima koneksi dari klien
            client_connection, client_address = server_socket.accept()
            print(f"Terhubung dengan {client_address}")

            # Menangani permintaan dari klien
            handle_client(client_connection)

if __name__ == "__main__":
    start_server()
