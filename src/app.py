from slackclient import SlackClient
from flask import Flask, request
import os
from SlackEvent import SlackEvent
from EventDispatcher import SlackEventDispatcher
import sqlite3
from peewee import *
from pprint import pprint
import time
import json
from rtm import *
from ANDREW import ANDREW
from workspace import Workspace
import asyncio
from threading import *
from command import *

#   Init enviroment vars
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
oauth_scope = os.environ["SLACK_BOT_SCOPE"]
verification_token = os.environ["SLACK_VERIFICATION_TOKEN"]
db = SqliteDatabase('../data/andrew')

class ping(RTMListener):
    def onMessage(self, event):
        if(event.data['text'] == "ping"):
            event.sc.rtm_send_message(event.data['channel'],'pong')

class commandHandler(CommandListener):
    def onCommand(self, event):
        sc = SlackClient(event.workspace.access_token)
        pprint(sc.api_call('api.test'))

# Register handlers here.
andrew = ANDREW()
andrew.registerRtmListener(ping)
andrew.registerCommandListener(commandHandler)
andrew.bootstrap()

app = Flask(__name__)


@app.route("/command/<command>", methods=["POST"])
def command_request(command):
    if(request.form["token"] != verification_token):
        return "", 401 

    commandWorkspace = Workspace.get(Workspace.team_id == request.form['team_id'])
    andrew.emitEvent(CommandEvent(CommandEvent.COMMANDSEND,request.form, commandWorkspace))
    return "", 200

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
    

    pprint(auth_response)
    workspace = Workspace(name =auth_response['team_name'], url = 'slack.com', access_token = workspace_access_token, bot_token = workspace_bot_token, team_id = auth_response['team_id'])
    workspace.save()


    return 'success';
    
