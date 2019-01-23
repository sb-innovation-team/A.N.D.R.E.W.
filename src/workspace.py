
from peewee import *
import os
db = SqliteDatabase(os.environ['DATABASE'])
class Workspace(Model):
    id = CharField()
    name = TextField()
    url = TextField()
    access_token = TextField()
    bot_token = TextField()
    team_id = TextField()
    class Meta:
        database = db