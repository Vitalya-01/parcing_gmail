from playhouse.sqlite_ext import *
from parcing_gmail.dataBase.models.BaseModel import BaseModel
from parcing_gmail.dataBase.models.Clients import Clients
from parcing_gmail.dataBase.models.MailInterlocutors import MailInterlocutors


class MailChains(BaseModel):
    id = AutoField()
    client_id = ForeignKeyField(column_name="client_id", field="id", model=Clients)
    interlocutor_id = ForeignKeyField(
        column_name="interlocutor_id", field="id", model=MailInterlocutors
    )
    data_thread_id = CharField(
        column_name="data_thread_id", max_length=255, null=False, unique=True
    )

    class Meta:
        table_name = "mail_chains"

    @classmethod
    def get_or_create_chain(cls, client_id, chain_id, interlocutor_id):
        chain, check = MailChains.get_or_create(
            client_id=client_id,
            interlocutor_id=interlocutor_id,
            data_thread_id=chain_id,
        )
        return chain
