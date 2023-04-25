from playhouse.sqlite_ext import *
import os


def get_db_instance():
    return SqliteDatabase('parcing_gmail.db')
