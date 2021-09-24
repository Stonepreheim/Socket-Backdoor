#written By Stone Preheim
import socket

ADDR = '23.123.182.6'#my public facing IPv4. If you are looking to test this dr. use loopback.
PORT = 7771 #only open when im running server

#setting up class structure for later after socket testing
class Client:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port

    def connectToServer(self):
        print("Attempting Connection: ")
        #need to learn about sockets and write socket tests will come back to this

    def sendTestPacket(ADDR, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((ADDR, PORT))
            soc.sendall(b'this should come back to me')  # casting to byte like object and sending packet
            data = soc.recv(1024)

        print('Server sent:', repr(data))

if __name__ == '__main__':
    #client = Client(ADDR, PORT)
    Client.sendTestPacket(ADDR, PORT)