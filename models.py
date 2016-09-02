from datetime import datetime
# import codecs, json
from peewee import *
from user import *

db = PostgresqlDatabase(User.db_name, **{'user': User.db_username, 'host': 'localhost', 'port': 5432,
                                    'password': User.db_passworld})

class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = db


class Story(BaseModel):
    story_title = TextField()
    user_title = TextField()
    acceptance_criteria = TextField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()
    date = DateTimeField(default=datetime.utcnow())

    @classmethod
    def get_story_id(cls, id):
        return cls.get(cls.id == id)
