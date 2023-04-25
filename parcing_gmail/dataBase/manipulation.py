from parcing_gmail.dataBase.db import get_db_instance
from parcing_gmail.dataBase.models.Clients import Clients
from parcing_gmail.dataBase.models.MailChains import MailChains
from parcing_gmail.dataBase.models.MailInterlocutors import MailInterlocutors
from parcing_gmail.dataBase.models.MailMessages import MailMessages


def create_tables():
    db = get_db_instance()
    if not db.table_exists(Clients):
        db.create_tables([Clients, MailInterlocutors, MailChains, MailMessages])


def add_client(first_name, last_name, email, password):
    return Clients.get_or_create_client(first_name, last_name, email, password)


def get_clients():
    return Clients.select()


def get_chains():
    return MailChains.select()


def get_interlocutors():
    return MailInterlocutors.select()


def get_messages():
    return MailMessages.select()
