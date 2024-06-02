from socket import *
import sys
import threading

def handle_client(connectionSocket):
    try:
        # Menerima data dari klien hingga 1024 byte dan mendekodenya menjadi string
        message = connectionSocket.recv(1024).decode()
        
        # Cetak informasi koneksi dan permintaan
        print(f"Terhubung dengan {connectionSocket.getpeername()}")  # Menampilkan alamat IP dan port klien
        print(f"Permintaan diterima: {message.splitlines()[0]}")  # Menampilkan baris pertama dari HTTP request
        host_info = next((line for line in message.splitlines() if line.startswith("Host: ")), "Host: Tidak Diketahui")
        print(host_info)  # Menampilkan informasi Host dari permintaan, atau Host: Tidak Diketahui" jika tidak ada
        print(f"Connection: {connectionSocket.getsockname()}")  # Menampilkan alamat IP dan port server
        
        # Memeriksa apakah pesan tidak kosong
        if len(message.split()) < 2:
            raise IOError
        
        # Mendapatkan nama file yang diminta
        filename = message.split()[1]
        # Membuka file yang diminta
        f = open(filename[1:], 'r')
        # Membaca isi file
        outputdata = f.read()
        
        # Mengirim satu baris header HTTP ke socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        
        # Mengirim konten dari file yang diminta ke klien
        connectionSocket.send(outputdata.encode())
        
    except IOError:
        # Mengirim pesan respons untuk file yang tidak ditemukan
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        connectionSocket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
        
    finally:
        # Menutup socket klien
        connectionSocket.close()

def start_server():
    # Membuat socket server TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # Mempersiapkan socket server
    serverPort = 1234
    serverHost = '127.0.0.15'
    
    serverSocket.bind((serverHost, serverPort))  # Mengikat socket ke alamat dan port tertentu
    serverSocket.listen(5)  # Mendengarkan hingga 5 koneksi

    print(f"Server berjalan di http://{serverHost}:{serverPort}")
    
    while True:
        # Menerima koneksi baru
        connectionSocket, addr = serverSocket.accept()
        print(f"Terhubung dengan {addr}")  # Menampilkan alamat IP dan port klien yang terhubung
        
        # Membuat thread baru untuk menangani permintaan klien
        client_thread = threading.Thread(target=handle_client, args=(connectionSocket,))
        client_thread.start()

    # Menutup socket server (kode ini tidak akan pernah tercapai karena loop while True)
    serverSocket.close()
    sys.exit()  # Mengakhiri program setelah mengirim data yang sesuai

if __name__ == "__main__":
    start_server()
