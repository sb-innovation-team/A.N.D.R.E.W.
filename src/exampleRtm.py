from rtm import RTMListener
from pprint import *
class exampleRtm(RTMListener):
    def onMessage(self, event):
        if(event.data['text'] == "ping"):
            event.sc.rtm_send_message(event.data['channel'],'pong')
            self.ANDREW.sendMessage(event.sc, channel= event.data['channel'],text="Hallo gozer")
