import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#rumah tersebut dan memakai tcp 
serverPort = 6789
serverSocket.bind(('localhost', serverPort))
serverSocket.listen(1)
print("Menunggu Seseorang...\r\n")

while True: 
   ConnectionSocket , addr = serverSocket.accept()
   message = ConnectionSocket.recv(1024).decode()
   print(message)
   try:
      filename = message.split()[1]
      f = open(filename[1:])
      outputdata = f.read()
      ConnectionSocket.sendall("HTTP/1.1 200 OK\r\n\r\n".encode())
      for i in range(0, len(outputdata)):
         ConnectionSocket.sendall(outputdata[i].encode())
      ConnectionSocket.sendall("\r\n".encode())
   except FileNotFoundError:
      ConnectionSocket.sendall("File not found".encode())

   ConnectionSocket.close()