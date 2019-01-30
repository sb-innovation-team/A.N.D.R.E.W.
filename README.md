# What is A.N.D.R.E.W?
A.N.D.R.E.W (Automated Neural Diagnostics and Reactive Electronics Webservice) is an attempt at making it easier to extend slack functionalities. Mainly for use at our office.


## How to create an ANDREW listener?
ANDREW has multiple types of listeners:
- RTM ( Listens to the real time messaging api from slack )
- Command ( Listens for command requests on the [url]/commands/[command] route)


### Example rtm listener ( [exampleRtm.py](https://github.com/sb-innovation-team/A.N.D.R.E.W./blob/master/src/exampleRtm.py) )
```python
from rtm import RTMListener

class exampleRtm(RTMListener):
    def onMessage(self, event):
        if(event.data['text'] == "ping"):
            event.sc.rtm_send_message(event.data['channel'],'pong')
```
It is as easy as extending the rtm listener and overriding the preset methods for each rtm event.
<br>
<br>

### Example command listener ( [exampleCommand.py](https://github.com/sb-innovation-team/A.N.D.R.E.W./blob/master/src/exampleCommand.py) )
```python
from command import CommandListener
from slackclient import *
from pprint import pprint

class exampleCommand(CommandListener):
    def onCommand(self, event):
        commandName = event.data['command']
        if(commandName == "/test"):
            sc = SlackClient(event.workspace.access_token)
            pprint(sc.api_call('api.test'))
```
On the command listeners is as easy as extending the command listener and overriding the onCommand method and checking wich command you are getting.

<br>
<br>

### You have to register each listener in [app.py](https://github.com/sb-innovation-team/A.N.D.R.E.W./blob/master/src/app.py)  as shown below
```python
andrew = ANDREW()

# Start of handlers here.

andrew.registerRtmListener(exampleRtm)
andrew.registerCommandListener(exampleCommand)

# End of handlers here.

andrew.bootstrap()
```
