from peewee import Model

from app import database

class BaseModel(Model):
    class Meta:
        database = database