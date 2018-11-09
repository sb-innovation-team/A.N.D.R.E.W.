from SlackEvent import SlackEvent
from EventDispatcher import SlackEventDispatcher

class CommandEvent(SlackEvent):
    COMMANDSEND = "command_send"

    def __init__(self, event_type, data, sc):
        self._type = event_type
        self._data = data
        self._sc = sc

    @property
    def data(self):
        return self._data
    
    @property
    def sc(self):
        return self._sc


class CommandListener(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.add_event_listener(
            CommandEvent.COMMANDSEND, self.onCommand
        )

    def onCommand(self, event):
        pass
