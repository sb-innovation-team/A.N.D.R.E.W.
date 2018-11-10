
from peewee import *
db = SqliteDatabase('../data/andrew')
class Workspace(Model):
    id = CharField()
    name = TextField()
    url = TextField()
    access_token = TextField()
    bot_token = TextField()
    team_id = TextField()
    class Meta:
        database = db