from app.models import BaseModel
from peewee import CharField, FloatField, PrimaryKeyField, TextField, DateTimeField, IntegerField

class Transaction(BaseModel):
    id = PrimaryKeyField()
    transaction_code = CharField()
    amount_brut = FloatField()
    amount_net = FloatField()
    payment_type = CharField()
    time = DateTimeField()
    products = TextField()
    status = CharField()