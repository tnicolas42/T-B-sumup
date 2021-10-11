import requests
from flask import Flask, request, redirect
import json
import exploit
import time
import datetime

app = Flask(__name__)

client_id = "hasTfAnVKbiidOJvJdMB-Y_UnTFO"
client_secret = "401471e85b6b03c2682de29b1c50161112cd77749c7ab73c524f92491bfef062"

url = f"https://api.sumup.com/authorize?response_type=code&client_id={client_id}&redirect_uri=http://127.0.0.1:5000/callback&scope=payments user.app-settings transactions.history user.profile_readonly&state=2cFCsY36y95lFHk4"


date_start = None
date_start = "2021-10-04T00:00:00.0"
date_end   = None
date_end   = "2021-10-08T23:59:59.0"

@app.route("/")
def main_route():
    return redirect(url)

def get_one_transaction(headers, transaction_code):
    base_url = 'https://api.sumup.com/v0.1/me/transactions?'
    params = f'transaction_code={transaction_code}'
    response = requests.get(f"{base_url}{params}", headers=headers)
    res = response.json()
    return res

def get_all_transaction(headers, start_time=None, end_time=None):
    base_url = "https://api.sumup.com/v0.1/me/transactions/history?"
    params = "order=descending&statuses[]=SUCCESSFUL&limits=1000"
    if start_time is not None:
        params += '&oldest_time=' + start_time
    if end_time is not None:
        params += '&newest_time=' + end_time
    items = []
    while True:
        response = requests.get(f"{base_url}{params}", headers=headers)
        res = response.json()
        items.extend(res["items"])
        next = res.get("links")
        if next:
            params = next[0]["href"]
        else:
            break

    new_items = []
    for idx, it in enumerate(items):
        if idx % 10 == 0:
            print(str(int(idx / len(items) * 100)) + "%")
        new_items.append(get_one_transaction(headers, it['transaction_code']))


    with open("result.json", "w") as f:
        json.dump(new_items, f)

    result = exploit.exploit(new_items)

    return result

@app.route("/callback")
def callback():
    code = request.args.get("code")

    d = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code
    }
    response = requests.post("https://api.sumup.com/token", data=d)
    access_token = response.json()["access_token"]
    headers = {
        'Authorization': 'Bearer {}'.format(access_token)
    }
    
    result = get_all_transaction(headers, date_start, date_end)
    # result = get_one_transaction(headers, transaction_code='TFMR2NCNXR')

    return str(result)


if __name__ == '__main__':
    app.run(debug=True)
