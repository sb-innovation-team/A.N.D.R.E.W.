
import requests
from pprint import pprint
import json
import random
from command import CommandListener
from slackclient import *
import time
import datetime
class quotesCommand(CommandListener):
    def onCommand(self, event):
        commandName = event.data['command']
        sc = SlackClient(event.workspace.bot_token)
        if(commandName == "/randomquote"):
            quote = randomQuote()            
            timestamp = time.mktime(datetime.datetime.strptime(quote['created_at'],"%Y-%m-%d %H:%M:%S").timetuple())
            res = sc.api_call('chat.postMessage', channel=event.data['channel_id'], attachments=[{
                "color": "#d44b1e",
                "text": quote['quote'],
                "footer": quote['author'],
                "ts": timestamp
            }])

        if(commandName == "/createQuote"):
            res = sc.api_call('chat.postMessage', channel=event.data['channel_id'], attachments=[{
                "color": "#d44b1e",
                "title": "Maak hieronder een nieuwe quote aan.",
            }])
            
def getQuotes():
    r = requests.get('https://quotesapi.sbdev.nl/quote/all')
    if(r.status_code == 200):
        return json.loads(r.text)

    else:
        return None

def createQuote(quote, author):
    r = requests.post('https://quotesapi.sbdev.nl/quote/create',{
        'quote': quote,
        'author': author
    })
    return r.status_code


def randomQuote():
    r = requests.get('https://quotesapi.sbdev.nl/quote/find')
    if(r.status_code == 200):
        return json.loads(r.text)

def getQuote():
    r = requests.get('https://quotesapi.sbdev.nl/quote/find/' + 1)
    print(r.text)    

if __name__ == "__main__":
    # testQuote = createQuote("Test", "Sascha achter zijn computer")
    # if(testQuote == 200):
    #     print("Quote toegevoegd")

    getQuote()