from playhouse.sqlite_ext import *
from parcing_gmail.dataBase.db import get_db_instance


class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = get_db_instance()