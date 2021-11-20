from app.models import BaseModel
from peewee import CharField, FloatField, PrimaryKeyField, TextField, DateTimeField, IntegerField
from playhouse.shortcuts import model_to_dict

class Transaction(BaseModel):
    # id = PrimaryKeyField()
    transaction_code = CharField()
    amount_brut = FloatField()
    amount_net = FloatField()
    payment_type = CharField()
    time = DateTimeField()
    products = TextField()
    status = CharField()

    def to_dict(self, exclude=None, include=None):
        """
        This base method is made to be overridden when you need something removed to added to the returned dictionary
        """
        if include is None:
            include = {}
        if exclude is None:
            exclude = []
        returned_dict = model_to_dict(self)
        for i in exclude:
            returned_dict.pop(i)
        for key, value in include.items():
            returned_dict[key] = value
        return returned_dict