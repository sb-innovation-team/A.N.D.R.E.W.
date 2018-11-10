from rtm import RTMListener

class exampleRtm(RTMListener):
    def onMessage(self, event):
        if(event.data['text'] == "ping"):
            event.sc.rtm_send_message(event.data['channel'],'pong')