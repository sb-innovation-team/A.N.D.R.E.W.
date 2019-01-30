class SlackMessage():
    def __init__(self, message):
        self._text = message
        self._attachements = {}
        pass

    def __str__(self):
        pass

    def getJson(self):
        pass

class SlackAttachement():
    def __init__(self):
        self._text = ""
        self._fallback = ""
        self._color = ""
        self._author_name = ""
        self._author_link = ""
        self._title = ""
        self._title_link = ""
        self._fields = {}
        self._image_url = ""
        self._thumb_url = ""
        self._footer = ""
        self._footer_icon = ""
        self._ts = ""


    def addField(self):
        pass

class SlackAttachementField():
    def __init__(self, title, value, short = False):
        self._title = title
        self._value = value
        self._short = short

    