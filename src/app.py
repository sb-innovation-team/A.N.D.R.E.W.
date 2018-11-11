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

# Import handler classes
from exampleCommand import exampleCommand
from exampleRtm import exampleRtm

#   Init enviroment vars
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]
oauth_scope = os.environ["SLACK_BOT_SCOPE"]
verification_token = os.environ["SLACK_VERIFICATION_TOKEN"]

# Load database
db = SqliteDatabase('../data/andrew')




# Register handlers here.
andrew = ANDREW()
andrew.registerRtmListener(exampleRtm)
andrew.registerCommandListener(exampleCommand)
andrew.bootstrap()

app = Flask(__name__)


# Handles all incomming commands
@app.route("/command/<command>", methods=["POST"])
def command_request(command):

    # Verify if the command is comming from slack
    if(request.form["token"] != verification_token):
        return "", 401 

    commandWorkspace = Workspace.get(Workspace.team_id == request.form['team_id'])
    andrew.emitEvent(CommandEvent(CommandEvent.COMMANDSEND,request.form, commandWorkspace))
    return "", 200


# Oauth step 1
@app.route("/begin_auth", methods=["GET"])
def pre_install():
  return '''
      <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
          Add to Slack
      </a>
  '''.format(oauth_scope, client_id)




# Oauth step 2 saving tokens and workspace
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
    
    workspace_access_token = auth_response['access_token']
    workspace_bot_token = auth_response['bot']['bot_access_token']

    # Add team to database   
    workspace = Workspace(name =auth_response['team_name'], url = 'slack.com', access_token = workspace_access_token, bot_token = workspace_bot_token, team_id = auth_response['team_id'])
    workspace.save()


    return 'success', 200   
    
