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
from command import *
from multiprocessing import Process
import multiprocessing as mp
import threading

class ANDREW:
    def __init__(self):
        self._threads = []
        self._event_dispatcher = SlackEventDispatcher()
        self._rtm_listeners = []
        self._message_listeners = []
        self._command_listeners = []
        self._rtmPollingrate = 0.5
        self._runRtm = True


    def bootstrap(self):
        self._runRtm = True
        print("Starting rtm listeners...")
        self._threads.clear()
        self.startRtm()
        for thread in self._threads:
            thread.start()
        print("Rtm listeners loaded.")

    # reload is broken for now..
    def reload(self):
        print("Stopping rtm listeners...")
        self.closeThreads()          
        print("Rtm listeners stopped.")
        self.bootstrap()

    def closeThreads(self):
        self._runRtm = False
        for thread in self._threads:
            thread.join()


    @property
    def rtmPollingrate(self, rtmPollingrate):
        self._rtmPollingrate = rtmPollingrate

    def registerRtmListener(self, rtmHandler: RTMListener):
        return rtmHandler(self._event_dispatcher, self)

    def registerCommandListener(self, commandHandler: CommandListener):
        return commandHandler(self._event_dispatcher)

    def emitEvent(self, event: SlackEvent):
        self._event_dispatcher.dispatch_event(
           event
        )

    def rtmListLoop(self, workspace):
        sc = SlackClient(workspace.bot_token)
        if sc.rtm_connect():
            while sc.server.connected == True and self._runRtm == True:
                for rtmevent in sc.rtm_read():
                    if('type' in rtmevent):
                        self.emitEvent(RTMEvent(rtmevent['type'], rtmevent,sc))
                time.sleep(self._rtmPollingrate)

    # Starts the rtm server for all of the servers and handles the rtm events.
    def startRtm(self):
        pprint(Workspace.select())
        for workspace in Workspace.select():
            _rtmThread = Process(target=self.rtmListLoop, args=(workspace,))
            _rtmThread.daemon = True
            self._threads.append(_rtmThread)

    def handleCommand(self, command, data):
        pass
        
