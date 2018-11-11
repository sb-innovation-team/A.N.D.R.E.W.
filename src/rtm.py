from SlackEvent import SlackEvent
from EventDispatcher import SlackEventDispatcher

class RTMEvent(SlackEvent):
    TYPING = "user_typing"
    MESSAGE = "message"
    FILE_SHARE = "file_shared"

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


class RTMListener(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        
        self.event_dispatcher.add_event_listener(
            RTMEvent.FILE_SHARE, self.onFileshare
        )

        self.event_dispatcher.add_event_listener(
            RTMEvent.TYPING, self.onTyping
        )

        self.event_dispatcher.add_event_listener(
            RTMEvent.MESSAGE, self.onMessage
        )

    def onTyping(self, event):
        pass

    def onMessage(self, event):
        pass

    def onFileshare(self, event):
        pass
