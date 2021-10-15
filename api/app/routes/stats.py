import pandas as pd
import datetime

from flask import Blueprint
from app.models.transaction import Transaction
from app import PAYMENT_TYPES
from app.utils.stats import get_total_from_query

stats_bp = Blueprint("stats", __name__)

@stats_bp.route("/stats/total", methods=["GET"])
def total_brut():
    query = Transaction.select()
    result = get_total_from_query(query)

    return result

@stats_bp.route("/stats/get_weeks", methods=["GET"])
def get_weeks():
    return {
        'weeks': pd.date_range(start=datetime.date(2021, 9, 20), end=datetime.datetime.now(), freq='W-MON').strftime('%d/%m/%Y').tolist(),
    }

@stats_bp.route("/stats/week/<week>/total", methods=["GET"])
def stats_week(week: str):
    """
    send date as dd_mm_yyyy
    """
    week = week.replace('_', '/')
    week_start = datetime.datetime.strptime(week, '%d/%m/%Y')
    week_end = week_start + datetime.timedelta(days=7)

    result = {}
    for payment_type in PAYMENT_TYPES:
        query = Transaction.select().where(Transaction.time > week_start, Transaction.time < week_end, Transaction.payment_type == payment_type)
        if len(query) == 0:
            continue
        tot = get_total_from_query(query)
        result[payment_type] = {
            'total_brut': tot['total_brut'],
            'total_net': tot['total_net'],
        }

    return result