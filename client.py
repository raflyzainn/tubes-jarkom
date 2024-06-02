from socket import *
import sys

def run_client(server_host, server_port, filename):
    # Membuat socket klien TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    try:
        # Membuat koneksi dengan server
        clientSocket.connect((server_host, server_port))

        # Mengirim permintaan HTTP GET
        request = f"GET /{filename} HTTP/1.1\r\nHost: {server_host}\r\n\r\n"
        clientSocket.sendall(request.encode())

        # Menerima respons dari server
        response = b""
        while True:
            data = clientSocket.recv(1024)
            if not data:
                break
            response += data

        # Menampilkan respons dari server
        print(response.decode())

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Menutup socket klien
        clientSocket.close()

if __name__ == "__main__":
    # Memeriksa argumen baris perintah
    if len(sys.argv) != 4:
        print("Usage: client.py server_host server_port filename")
        sys.exit(1)

    # Mendapatkan argumen dari baris perintah
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    # Menjalankan fungsi klien
    run_client(server_host, server_port, filename)
