from playhouse.postgres_ext import *
from dataBase.models.BaseModel import BaseModel
from dataBase.models.Proxies import Proxies
from dataBase.models.Actors import Actors


class Clients(BaseModel):
    id = AutoField()
    actor_id = ForeignKeyField(column_name="actor_id", field="id", model=Actors)
    first_name = CharField()
    last_name = CharField()
    email_login = CharField()
    email_password = CharField()

    class Meta:
        table_name = "clients"
