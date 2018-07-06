from slackclient import SlackClient
from flask import Flask, request
import os
from SlackEventDispatcher import SlackEventDispatcher
from SlackEvent import SlackEvent
import sqlite3
from peewee import *

#   Init enviroment vars
slack_token = os.environ.get('SLACK_API_TOKEN')
client_id = os.environ.get("SLACK_CLIENT_ID")
client_secret = os.environ.get("SLACK_CLIENT_SECRET")
oauth_scope = os.environ.get("SLACK_BOT_SCOPE")

db = SqliteDatabase('andrew')

class Workspace(Model):
    id = CharField()
    class Meta:
        database = db


class SlackWorkspace():
    def __init__(self, name, url, access_token, bot_token):
        self._name = name
        self._url = url
        self._bot_token = bot_token
        self._access_token = access_token

# Een slack message event.
class MessageEvent(SlackEvent):
    SENT     = "sent"
    RECEIVED = "received"

# Extensie van slackevent, deze voegt simpelweg wat properties toe.
class CommandEvent(SlackEvent):
    EXCECUTED = "commandExcecuted"

    def __init__(self, event_type, command, url, data=None):
        self._type = event_type
        self._data = data
        self._url = url
        self._command = command

    @property
    def url(self):
        return self._url

    @property
    def command(self):
        return self._command


# Zo kunnen we easy voor commands listenen vanuit een http service van flask. dit maakt alles meer schaalbaar
class CommandListener(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher
        # Zo add je een listener aan je dispatcher
        self.event_dispatcher.add_event_listener(
            CommandEvent.EXCECUTED, self.onCommand
        )

    def onCommand(self, event):
            print(event.data)



class MessageListener(object):
    def __init__(self, event_dispatcher):
        self.event_dispatcher = event_dispatcher

        self.event_dispatcher.add_event_listener(
            MessageEvent.SENT, self.on_message_sent
        )

    def emit(self, data):
        self.event_dispatcher.dispatch_event(
           CommandEvent(CommandEvent.EXCECUTED, 'testCommand', 'https://test.me',data)
        )

    def on_message_sent(self, event):
        print(event.data)


dispatcher = SlackEventDispatcher()
messageListener = MessageListener(dispatcher)
commandListener = CommandListener(dispatcher)
app = Flask(__name__)

@app.route("/begin_auth", methods=["GET"])
def pre_install():
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

    # Sla hier je access tokens op.
    workspace_access_token = auth_response['access_token']
    workspace_bot_token = auth_response['bot']['bot_access_token']

    workspace = SlackWorkspace('Social Brothers','socialbrothers.slack.com', workspace_access_token, workspace_bot_token)

    
