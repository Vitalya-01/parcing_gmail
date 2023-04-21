from playhouse.postgres_ext import *
from dataBase.db import instance
import os


class BaseModel(Model):
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        database = instance
        schema = os.getenv("SCHEMA")
