from command import CommandListener
from slackclient import *
from pprint import pprint

class exampleCommand(CommandListener):
    def onCommand(self, event):
        commandName = event.data['command']
        if(commandName == "/test"):
            sc = SlackClient(event.workspace.access_token)
            pprint(sc.api_call('api.test'))
            