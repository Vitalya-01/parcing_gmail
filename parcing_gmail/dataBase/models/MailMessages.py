from playhouse.postgres_ext import *
from dataBase.models.BaseModel import BaseModel
from dataBase.models.MailChains import MailChains


class MailMessages(BaseModel):
    id = AutoField()
    chains_id = ForeignKeyField(column_name="chains_id", field="id", model=MailChains)
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
        messages = MailMessages.select().where(MailMessages.chains_id == chain_id)
        return messages

    @classmethod
    def add_to_db(cls, chain_id, message_id, text, is_interlocutor=False):
        is_exist = MailMessages.get_or_none(
            MailMessages.data_legacy_message_id == message_id
        )

        if is_exist is None:
            max_serial_number = (
                MailMessages.select(fn.Max(MailMessages.serial_number))
                .where(MailMessages.chains_id == chain_id)
                .scalar()
            )
            if max_serial_number is None:
                max_serial_number = 0
            MailMessages.create(
                chains_id=chain_id,
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
            MailMessages.chains_id == chain_id,
            MailMessages.data_legacy_message_id == message_id,
        )
        # print(message_id, chain_id)
        # print(check)
        if check is None:
            return True
        return False
