from flask import Flask
from peewee import SqliteDatabase
from flask_cors import CORS
from dotenv import dotenv_values
from redis import StrictRedis

##### SETTINGS #####
config = dotenv_values(".env")

CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]

PAYMENT_TYPES = { "CASH": "CASH", "CB": "CB", "PMK": "PMK" }
PAYMENT_COMMISSION = { "CASH": 0, "CB": 1.5, "PMK": 0.7 }

##### STARTING ALL #####
database = SqliteDatabase(database="db_sumup.db")

application = Flask(__name__)
CORS(application)

redis = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

##### APPLICATION CONFIG #####
from app.routes.connect import connect_bp
from app.routes.transactions import transactions_bp
from app.routes.stats import stats_bp

application.register_blueprint(connect_bp)
application.register_blueprint(transactions_bp)
application.register_blueprint(stats_bp)

##### DATABASE CONFIG #####
from app.models.transaction import Transaction

def create_tables():
    with database:
        database.create_tables([
            Transaction,
        ])

create_tables()

##### REDIS CONFIG #####
redis.set('redirect_url', '')