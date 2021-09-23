#written By Stone Preheim
import socket

HOST = '23.123.182.6'#my public facing IPv4, nobody DDOS plz if i share in class lol
PORT = 7771 #only open when im running server

#setting up class structure for later after socket testing
class Client:
    def __init__(self, addr, port):
        print("Will write this later gonna play with sockets")
    def connectToServer(self):
        print("Attempting Connection: ")

    def sendTestPacket(HOST, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((HOST, PORT))
            soc.sendall(b'this should come back to me')  # casting to byte like object and sending packet
            data = soc.recv(1024)

        print('Received', repr(data))

if __name__ == '__main__':
    #client = Client(HOST, PORT)
    Client.sendTestPacket(HOST, PORT)