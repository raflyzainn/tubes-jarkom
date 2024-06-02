import socket
import os
import threading

# Konfigurasi server
HOST = '127.0.0.1'  # Alamat IP lokal
PORT = 8080         # Port untuk server
BASE_DIR = '.'      # Direktori dasar untuk mencari file

def handle_request(client_socket):
    try:
        # Menerima permintaan dari klien
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Permintaan diterima: {request}")

        # Parse permintaan HTTP
        headers = request.split('\r\n')
        first_line = headers[0]
        method, path, version = first_line.split()

        # Hanya menangani metode GET
        if method != 'GET':
            # Menangani permintaan yang tidak diperbolehkan
            response_line = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
            client_socket.sendall(response_line.encode('utf-8'))
            return

        # Mendapatkan path file yang diminta
        file_path = os.path.join(BASE_DIR, path.strip('/'))

        if not os.path.isfile(file_path):
            # Menangani jika file tidak ditemukan
            response_line = "HTTP/1.1 404 Not Found\r\n\r\n"
            body = "<h1>404 Not Found</h1>".encode('utf-8')
            client_socket.sendall(response_line.encode('utf-8') + body)
            return

        # Membaca isi file
        with open(file_path, 'rb') as f:
            body = f.read()

        # Membuat respons HTTP
        response_line = "HTTP/1.1 200 OK\r\n"
        headers = "Content-Length: {}\r\n".format(len(body))
        headers += "Content-Type: text/html\r\n"  # Anggap semua file adalah HTML untuk kesederhanaan
        headers += "\r\n"

        # Mengirimkan respons ke klien
        client_socket.sendall(response_line.encode('utf-8') + headers.encode('utf-8') + body)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Menutup koneksi dengan klien
        client_socket.close()

def run_server():
    # Membuat socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Mengikat socket ke alamat dan port
        server_socket.bind((HOST, PORT))
        # Mendengarkan koneksi masuk
        server_socket.listen(5)
        print(f"Server berjalan di http://{HOST}:{PORT}")

        while True:
            # Menerima koneksi dari klien
            client_socket, client_address = server_socket.accept()
            print(f"Terhubung dengan {client_address}")
            # Membuat thread baru untuk menangani permintaan klien
            client_thread = threading.Thread(target=handle_request, args=(client_socket,))
            client_thread.start()

if __name__ == "__main__":
    run_server()
