from playhouse.sqlite_ext import *
from parcing_gmail.dataBase.models.BaseModel import BaseModel


class Clients(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    email_login = CharField()
    email_password = CharField()

    class Meta:
        table_name = "clients"

    @classmethod
    def get_or_create_client(cls, first_name, last_name, email_login, email_password):
        client, check = Clients.get_or_create(
            first_name=first_name,
            last_name=last_name,
            email_login=email_login,
            email_password=email_password,
        )
        return client