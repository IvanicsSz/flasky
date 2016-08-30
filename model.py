import datetime
from peewee import *
from main import *

class Note(db.Model):
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now)