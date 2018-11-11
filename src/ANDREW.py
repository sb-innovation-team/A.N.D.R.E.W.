from slackclient import SlackClient
from flask import Flask, request
import os
from EventDispatcher import SlackEventDispatcher
from SlackEvent import SlackEvent
from workspace import Workspace
from enum import Enum
from rtm import RTMListener
import time
from pprint import pprint
from rtm import RTMEvent
from threading import *
from command import *
listenerTypes = Enum('RTM', 'Command')

class ANDREW:
    def __init__(self):
        self._event_dispatcher = SlackEventDispatcher()
        self._rtm_listeners = []
        self._message_listeners = []
        self._command_listeners = []
        self._rtmPollingrate = 0.5


    def bootstrap(self):
        t = Thread(target=self.startRtm)
        t.daemon = True
        t.start()

    @property
    def rtmPollingrate(self, rtmPollingrate):
        self._rtmPollingrate = rtmPollingrate

    @staticmethod
    def listenerTypes():
        return listenerTypes

    def registerRtmListener(self, rtmHandler: RTMListener):
        return rtmHandler(self._event_dispatcher)

    def registerCommandListener(self, commandHandler: CommandListener):
        return commandHandler(self._event_dispatcher)

    def emitEvent(self, event: SlackEvent):
        self._event_dispatcher.dispatch_event(
           event
        )
    
    # Starts the rtm server for all of the servers and handles the rtm events.
    def startRtm(self):
        for workspace in Workspace.select():
            sc = SlackClient(workspace.bot_token)
            if sc.rtm_connect():
                while sc.server.connected is True:
                    for rtmevent in sc.rtm_read():
                        if('type' in rtmevent):
                            self.emitEvent(RTMEvent(rtmevent['type'], rtmevent,sc))
                    time.sleep(self._rtmPollingrate)


    def handleCommand(self, command, data):
        pass
        
