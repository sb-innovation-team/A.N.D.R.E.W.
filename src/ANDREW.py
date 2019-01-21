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
import threading

class ANDREW:
    def __init__(self):
        self._thread = None
        self._event_dispatcher = SlackEventDispatcher()
        self._rtm_listeners = []
        self._message_listeners = []
        self._command_listeners = []
        self._rtmPollingrate = 0.5
        self._runRtm = True


    def bootstrap(self):
        self._runRtm = True
        self._thread = Thread(target=self.startRtm)
        self._thread.daemon = True
        self._thread.start()


    def reload(self):
        print("Reloading rtm listeners....")
        self._runRtm = False
        time.sleep(1)
        self.bootstrap()
        print("Reloading complete!")

        
    @property
    def rtmPollingrate(self, rtmPollingrate):
        self._rtmPollingrate = rtmPollingrate

    def registerRtmListener(self, rtmHandler: RTMListener):
        return rtmHandler(self._event_dispatcher)

    def registerCommandListener(self, commandHandler: CommandListener):
        return commandHandler(self._event_dispatcher)

    def emitEvent(self, event: SlackEvent):
        self._event_dispatcher.dispatch_event(
           event
        )

    def rtmListLoop(self, workspace):
        sc = SlackClient(workspace.bot_token)
        if sc.rtm_connect():
            while sc.server.connected == True and self._runRtm is True:
                for rtmevent in sc.rtm_read():
                    if('type' in rtmevent):
                        self.emitEvent(RTMEvent(rtmevent['type'], rtmevent,sc))
                time.sleep(self._rtmPollingrate)

    # Starts the rtm server for all of the servers and handles the rtm events.
    def startRtm(self):
        pprint(Workspace.select())
        for workspace in Workspace.select():
            _rtmThread = threading.Thread(target=self.rtmListLoop, args=(workspace,))
            _rtmThread.start()

    def handleCommand(self, command, data):
        pass
        
