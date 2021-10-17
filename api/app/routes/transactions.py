import requests

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
    sumup_code = request.args.get("sumup_code")

    d = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": sumup_code
    }
    response = requests.post("https://api.sumup.com/token", data=d)
    if response.status_code != 200:
        return response.text, 500
    access_token = response.json()["access_token"]
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    
    ok, content = get_all_sumup_transactions(headers)
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

    return query.to_dict()
