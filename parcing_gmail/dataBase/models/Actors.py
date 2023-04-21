from playhouse.postgres_ext import *
from dataBase.models.BaseModel import BaseModel


class Actors(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    email = CharField()
    email_password = CharField()

    class Meta:
        table_name = "actors"
