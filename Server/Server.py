#Written by Stone Preheim
import socket

HOST = '192.168.1.77'#portforwarding FTW!
PORT = 7771

#setting up class structure for later after socket testing
class Server:
    def __init__(self, addr, port):
        print("Will write this later gonna play with sockets")
    def startServer(self):
        print("Starting Server: ")

    def testSocket(HOST, PORT):
        with socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM) as soc:  # creating socket with ipv4 and tcp. Need to reconfigure this to not use blocking.
            soc.bind((HOST, PORT))
            soc.listen()
            print("server is listening.... quietly...")
            conn, address = soc.accept()
            with conn:
                print("Connected to:", address)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print("Received: " + repr(data))
                    conn.sendall(data)

if __name__ == '__main__':
    #serv = Server(HOST, PORT)
    Server.testSocket(HOST, PORT)