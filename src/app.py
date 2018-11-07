from slackclient import SlackClient
from flask import Flask, request
import os
from SlackEventDispatcher import SlackEventDispatcher
from SlackEvent import SlackEvent
import sqlite3
from peewee import *
from pprint import pprint
import time
import json
#   Init enviroment vars
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
oauth_scope = os.environ["SLACK_BOT_SCOPE"]

db = SqliteDatabase('../data/andrew')


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

    def emit(self, eventType, data, sc):
        self.event_dispatcher.dispatch_event(
           RTMEvent(eventType,data, sc)
        )



class myRtmHandler(RTMListener):
    def onTyping(self, event):
        pprint(event.data['user'])

    def onMessage(self, event):
        event.sc.rtm_send_message(event.data['channel'], "Hallo broeder")



dispatcher = SlackEventDispatcher()
rtmListener = myRtmHandler(dispatcher)


class Workspace(Model):
    id = CharField()
    name = TextField()
    url = TextField()
    access_token = TextField()
    bot_token = TextField()
    class Meta:
        database = db

for workspace in Workspace.select():
    sc = SlackClient(workspace.bot_token)

    if sc.rtm_connect():
        while sc.server.connected is True:
            for rtmevent in sc.rtm_read():
                if('type' in rtmevent):
                    rtmListener.emit(rtmevent['type'], rtmevent,sc)
            time.sleep(0.4)

class SlackWorkspace():
    def __init__(self, name, url, access_token, bot_token):
        self._name = name
        self._url = url
        self._bot_token = bot_token
        self._access_token = access_token


app = Flask(__name__)



@app.route("/begin_auth", methods=["GET"])
def pre_install():
  print(client_id);

  return '''
      <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
          Add to Slack
      </a>
  '''.format(oauth_scope, client_id)



@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    auth_code = request.args['code']    

    sc = SlackClient("")

    auth_response = sc.api_call(
        "oauth.access", 
        client_id=client_id,
        client_secret=client_secret,
        code=auth_code
    )
    
    pprint(auth_response);
    # Sla hier je access tokens op.
    workspace_access_token = auth_response['access_token']
    workspace_bot_token = auth_response['bot']['bot_access_token']

    workspace = Workspace(name ='Social Brothers',url = 'socialbrothers.slack.com', access_token = workspace_access_token, bot_token = workspace_bot_token)
    workspace.save()


    return 'success';
    
