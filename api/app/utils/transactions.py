import json
import requests
import unidecode
import dateutil.parser

from app import PAYMENT_TYPES, PAYMENT_COMMISSION
from app.models.transaction import Transaction


def add_transaction(headers, transaction_code):
    base_url = 'https://api.sumup.com/v0.1/me/transactions?'
    params = f'transaction_code={transaction_code}'
    response = requests.get(f"{base_url}{params}", headers=headers)
    if response.status_code != 200:
        return False, response.text
    res = response.json()

    products = {}

    prod = res['product_summary']
    prod = prod.split(',')
    for p in prod:
        p2 = p.split(" x ")
        nb = int(p2[0].strip())

        pp2 = p2[1].split(' ')
        payment_type = pp2[0].strip()
        if payment_type in PAYMENT_TYPES:
            try:
                int(pp2[1])
                name = ' '.join(pp2[2:])
            except ValueError:
                name = ' '.join(pp2[1:])
        else:
            if res['payment_type'] == 'CASH':
                payment_type = PAYMENT_TYPES["CASH"]
            else:
                payment_type = PAYMENT_TYPES["CB"]
            if p2[1].strip().startswith("Custom amount") \
                or p2[1].strip().startswith("Montant personnalis"):
                name = "Custom"
            else:
                name = p2[1]
        name = name.strip().lower()
        name = unidecode.unidecode(name)
        products[name] = nb

    amount_net = res["amount"] * (1 - (PAYMENT_COMMISSION[payment_type] / 100))

    Transaction.create(
        id=res["internal_id"],
        transaction_code=res["transaction_code"],
        amount_brut=res["amount"],
        amount_net=amount_net,
        payment_type=payment_type,
        time=dateutil.parser.parse(res["local_time"]),
        products=json.dumps(products),
        status=res["simple_status"],
    )
    return True, 'OK'

def get_all_sumup_transactions(headers, start_time=None, end_time=None):
    limits = 1000
    base_url = "https://api.sumup.com/v0.1/me/transactions/history?"
    params = f"order=descending&statuses[]=SUCCESSFUL&limits={limits}"
    if start_time is not None:
        params += '&oldest_time=' + start_time
    if end_time is not None:
        params += '&newest_time=' + end_time
    items = []
    while True:
        response = requests.get(f"{base_url}{params}", headers=headers)
        if response.status_code != 200:
            return False, response.text
        res = response.json()
        items.extend(res["items"])
        next = res.get("links")
        if next:
            params = next[0]["href"]
        else:
            break

    for idx, it in enumerate(items):
        if idx % 10 == 0:
            print('[%3d%%] %d/%d' % (int(float(idx) / len(items) * 100), idx, len(items)))
        transactions = Transaction.select().where(Transaction.transaction_code == it["transaction_code"])
        if len(list(transactions)) == 0:
            ok, content = add_transaction(headers, it['transaction_code'])
            if not ok:
                return ok, content
    return True, 'OK'