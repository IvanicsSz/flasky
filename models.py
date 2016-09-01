from datetime import datetime
# import codecs, json
from peewee import *

db = PostgresqlDatabase('story', **{'user': "szilard", 'host': 'localhost', 'port': 5432,
                                    'password': '753951'})

class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Story(BaseModel):
    story_title = TextField()
    user_title = TextField()
    acceptance_criteria = TextField()
    business_value = BigIntegerField()
    estimation = SmallIntegerField()
    status = CharField()
    date = DateTimeField(default=datetime.utcnow())
