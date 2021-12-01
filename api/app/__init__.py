from flask import Flask
from peewee import SqliteDatabase
from flask_cors import CORS
from dotenv import dotenv_values
from redis import StrictRedis

##### SETTINGS #####
config = dotenv_values(".env")

CLIENT_ID = config["CLIENT_ID"]
CLIENT_SECRET = config["CLIENT_SECRET"]
RUNNING_PORT = config["API_PORT"]

PAYMENT_TYPES = { "CASH": "CASH", "CB": "CB", "PMK": "PMK" }
PAYMENT_COMMISSION = { "CASH": 0, "CB": 1.5, "PMK": 0.7 }

##### GOOGLE SHEETS UTILS #####
from app.utils.google_sheets_api import GoogleSheetsApi

gsheet = GoogleSheetsApi().connect_api()

# info on tbcompte spreadsheet
class TBCOMPTE:
    CHARGES = dict(
        file_id='1zsZkhHlK6W4paS4rsML95iym615kD2WVRnNMjJ2H1PA',
        sheet_name='Charges',
    )
    PRODUITS = dict(
        file_id='1zsZkhHlK6W4paS4rsML95iym615kD2WVRnNMjJ2H1PA',
        sheet_name='Produits',
    )
    INFO_REPAS = dict(
        file_id='1zsZkhHlK6W4paS4rsML95iym615kD2WVRnNMjJ2H1PA',
        sheet_name='Info repas',
    )
    TEST = dict(
        file_id='1zsZkhHlK6W4paS4rsML95iym615kD2WVRnNMjJ2H1PA',
        sheet_name='test',
    )

##### STARTING ALL #####
import logging
database = SqliteDatabase(database="db_sumup.db")

# cors = CORS()

application = Flask(__name__)
# cors.init_app(application)
# CORS(application)
CORS(
    application,
    allow_headers="*",
    origins="*",
    headers="*",
    expose_headers="*",
    supports_credentials=True,
)

logging.getLogger('flask_cors').level = logging.DEBUG

redis = StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

##### APPLICATION CONFIG #####
from app.routes.connect import connect_bp
from app.routes.transactions import transactions_bp
from app.routes.stats import stats_bp
from app.routes.compte import compte_bp
from app.routes.recipe import recipe_bp

application.register_blueprint(connect_bp)
application.register_blueprint(transactions_bp)
application.register_blueprint(stats_bp)
application.register_blueprint(compte_bp)
application.register_blueprint(recipe_bp)

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
redis.set('header_sumup', '')
redis.set('sumup_token_info', '')