class SlackEvent(object):
    def __init__(self, event_type, data=None):
        self._type = event_type
        self._data = data

    @property
    def type(self):
        return self._type

    @property
    def data(self):
        return self._data