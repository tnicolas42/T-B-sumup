import datetime
import dateutil
import json

from flask import Blueprint
from flask import request
from werkzeug.utils import redirect

from app import CLIENT_ID, CLIENT_SECRET, redis
from app.models.transaction import Transaction
from app.utils.transactions import get_all_sumup_transactions

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/transactions/fetch_all")
def fetch_all_transactions():
    print("fetching all new data...")
    
    # get last transaction time
    query = Transaction.select().order_by(-Transaction.time).first()
    start_time = None
    if query is not None:
        start_time = (dateutil.parser.parse(query.time) + datetime.timedelta(seconds=1)).strftime("%Y-%m-%dT%H:%M:%S.0")

    header = redis.get('header_sumup')
    if header == '':
        return "You are not connected", 401
    ok, content = get_all_sumup_transactions(json.loads(redis.get('header_sumup')), start_time=start_time)
    if not ok:
        return content, 500

    print("new transactions saved in database")

    return "All data fetched", 200

@transactions_bp.route("/transactions/size", methods=["GET"])
def get_nb_transactions():
    query = Transaction.select()
    return { 'size': len(query) }

@transactions_bp.route("/transactions/get/last", methods=["GET"])
def get_last_transaction():
    query = Transaction.select().order_by(-Transaction.time).first()

    if query is None:
        return {}

    return query.to_dict()
