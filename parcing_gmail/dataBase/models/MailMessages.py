from playhouse.sqlite_ext import *
from parcing_gmail.dataBase.models.BaseModel import BaseModel
from parcing_gmail.dataBase.models.MailChains import MailChains


class MailMessages(BaseModel):
    id = AutoField()
    chain_id = ForeignKeyField(column_name="chain_id", field="id", model=MailChains)
    data_legacy_message_id = CharField(
        column_name="data_legacy_message_id", max_length=255, null=False, unique=True
    )
    is_interlocutors = BooleanField(column_name="is_interlocutors", null=False)
    text = TextField()
    serial_number = SmallIntegerField()

    class Meta:
        table_name = "mail_messages"

    @classmethod
    def get_from_chain(cls, chain_id):
        messages = MailMessages.select().where(MailMessages.chain_id == chain_id)
        return messages

    @classmethod
    def add_to_db(cls, chain_id, message_id, text, is_interlocutor=False):
        is_exist = MailMessages.get_or_none(
            MailMessages.data_legacy_message_id == message_id
        )

        if is_exist is None:
            max_serial_number = (
                MailMessages.select(fn.Max(MailMessages.serial_number))
                .where(MailMessages.chain_id == chain_id)
                .scalar()
            )
            if max_serial_number is None:
                max_serial_number = 0
            MailMessages.create(
                chain_id=chain_id,
                data_legacy_message_id=message_id,
                is_interlocutors=is_interlocutor,
                text=text,
                serial_number=max_serial_number + 1,
            )
        else:
            print("Something go wrong\nMessage exist!\n")

    @classmethod
    def is_not_exist(cls, message_id, chain_id):
        check = MailMessages.get_or_none(
            MailMessages.chain_id == chain_id,
            MailMessages.data_legacy_message_id == message_id,
        )
        if check is None:
            return True
        return False
