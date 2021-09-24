#Written by Stone Preheim
import socket

ADDR = '192.168.1.77'#portforwarding FTW! if you are looking to test this dr. use loopback
PORT = 7771

#setting up class structure for later after socket testing
class Server:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port

    def startServer(self):
        print("Starting Server...")
        #need to learn about sockets and write socket tests will come back to this


    def testSocket(ADDR, PORT):
        with socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM) as soc:  #creating socket with ipv4 and tcp. Need to reconfigure this to not use blocking.
            soc.bind((ADDR, PORT))
            soc.listen()
            print("server is listening.... quietly...")
            conn, address = soc.accept()
            with conn:
                print("Connected to:", address)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print("Client sent:" + repr(data))
                    conn.sendall(data)

if __name__ == '__main__':
    #serv = Server(ADDR, PORT)
    Server.testSocket(ADDR, PORT)