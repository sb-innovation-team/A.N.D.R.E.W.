from SlackEvent import SlackEvent
from EventDispatcher import SlackEventDispatcher

class RTMEvent(SlackEvent):
    TYPING              =           "user_typing"
    MESSAGE             =           "message"
    FILE_SHARE          =           "file_shared"
    REACTION_ADDED      =           "reaction_added"
    STAR_ADDED          =           "star_added"
    CHANNEL_CREATED     =           "channel_created"
    CHANNEL_DELETED     =           "channel_deleted"
    CHANNEL_JOINED      =           "channel_joined"
    CHANNEL_LEFT        =           "channel_left"


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
    def __init__(self, event_dispatcher, ANDREW):
        self.event_dispatcher = event_dispatcher
        self.ANDREW = ANDREW

        self.event_dispatcher.add_event_listener(
            RTMEvent.FILE_SHARE, self.onFileshare
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.TYPING, self.onTyping
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.MESSAGE, self.onMessage
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.REACTION_ADDED, self.onReaction
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.STAR_ADDED, self.onStar
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.CHANNEL_CREATED, self.onChannelCreate
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.CHANNEL_DELETED, self.onChannelDelete
        )
        self.event_dispatcher.add_event_listener(
            RTMEvent.CHANNEL_JOINED, self.onChannelJoin
        )

        self.event_dispatcher.add_event_listener(
            RTMEvent.CHANNEL_LEFT, self.onChannelLeave
        )
        

    def onTyping(self, event):
        pass

    def onMessage(self, event):
        pass

    def onFileshare(self, event):
        pass

    def onReaction(self, event):
        pass

    def onStar(self, event):
        pass

    def onChannelCreate(self, event):
        pass

    def onChannelDelete(self, event):
        pass

    def onChannelJoin(self, event):
        pass

    def onChannelLeave(self, event):
        pass
