import socket
import threading
import sys
import os


class Server:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connections = []

    def __init__(self):
        self.sock.bind(('0.0.0.0', 10000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                if connection != c:
                    connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        if sys.platform == 'linux':
            os.system('clear')
        elif sys.platform == 'win32' or 'cygwin':
            os.system('cls')
        print("Server started successfully\n")
        while True:
            c, a = self.sock.accept()
            c_thread = threading.Thread(target=self.handler, args=(c, a))
            c_thread.daemon = True
            c_thread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")


class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_msg(self):
        while True:
            self.sock.send(bytes(self.client_name + ' sent a message: ' + input(""), 'utf-8'))

    def __init__(self, address):
        self.sock.connect((address, 10000))
        self.client_name = input("What is your name: ")
        if sys.platform == 'linux':
            os.system('clear')
        elif sys.platform == 'win32' or 'cygwin':
            os.system('cls')

        i_thread = threading.Thread(target=self.send_msg)
        i_thread.daemon = True
        i_thread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break
            print(str(data, 'utf-8'))


if len(sys.argv) > 1:
    client = Client(sys.argv[1])
else:
    server = Server()
    server.run()
