from playhouse.postgres_ext import *
from dataBase.models.BaseModel import BaseModel


class MailInterlocutors(BaseModel):
    id = AutoField()
    first_name = CharField()
    last_name = CharField()
    email = TextField()
    avatar_link = TextField()

    class Meta:
        table_name = "mail_interlocutors"

    @classmethod
    def get_or_create_interlocutor(cls, first_name, last_name, email, avatar_link):
        is_exist = MailInterlocutors.get_or_none(MailInterlocutors.email == email)
        if is_exist is None:
            interlocutor = MailInterlocutors.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                avatar_link=avatar_link,
            )
            return interlocutor
        return is_exist
