import pandas as pd
import datetime

from flask import Blueprint
from flask import request
from app.models.transaction import Transaction
from app import PAYMENT_TYPES
from app.utils.stats import get_total_from_query, get_stats_from_query

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

    result = {
        'total_brut': 0,
        'total_net': 0,
        'payment_type': {},
    }
    for payment_type in PAYMENT_TYPES:
        query = Transaction.select().where(Transaction.time > week_start, Transaction.time < week_end, Transaction.payment_type == payment_type)
        if len(query) == 0:
            continue
        tot = get_total_from_query(query)
        result['payment_type'][payment_type] = {
            'total_brut': tot['total_brut'],
            'total_net': tot['total_net'],
        }
        result['total_brut'] += tot['total_brut']
        result['total_net'] += tot['total_net']

    return result

@stats_bp.route("/stats/interval", methods=["GET"])
def stats_interval():
    """
    ?start_date=20_09_2021 <- date included
    ?end_date=20_09_2021 <- date included
    no data for all stats
    """
    # getting starting date
    start_date = request.args.get('start_date')
    if start_date is None:
        start_date = datetime.datetime.strptime('01/01/2021', '%d/%m/%Y')
    else:
        start_date = datetime.datetime.strptime(start_date.replace('_', '/'), '%d/%m/%Y')

    # getting ending date
    end_date = request.args.get('end_date')
    if end_date is None:
        end_date = datetime.datetime.now()
    else:
        end_date = datetime.datetime.strptime(end_date.replace('_', '/'), '%d/%m/%Y') + datetime.timedelta(days=1)

    query = Transaction.select().where(Transaction.time > start_date, Transaction.time < end_date)
    result = get_stats_from_query(query=query)

    return result