import datetime
import requests
import json

from flask import Blueprint
from flask import redirect, request, url_for

from app import CLIENT_ID, CLIENT_SECRET, redis

connect_bp = Blueprint("connect", __name__)

redirect_url = None

@connect_bp.route("/")
def main_route():
    return "home", 200

@connect_bp.route("/connect")
def connect():
    url = f"https://api.sumup.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/callback&scope=payments user.app-settings transactions.history user.profile_readonly&state=2cFCsY36y95lFHk4"
    return redirect(url)

@connect_bp.route("/get_connect_url")
def get_connect_url():
    url = f"https://api.sumup.com/authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://127.0.0.1:5000/callback&scope=payments"
    return url, 200

@connect_bp.route("/set_redirect_url")
def set_redirect_url():
    global redirect_url
    redis.set('redirect_url', request.args.get("url"))
    return "Success", 200


@connect_bp.route('/reconnect')
def reconnect():
    print("Reconnection...")
    if redis.get('sumup_token_info') != '':
        token_info = json.loads(redis.get('sumup_token_info'))
        d = {
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": token_info['code'],
            "refresh_token": token_info['refresh_token'],
        }
        response = requests.post("https://api.sumup.com/token", data=d)
        if response.status_code != 200:
            return response.text, 500
        response = response.json()
        response['expires_time'] = (datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'] - 5)).timestamp()
        access_token = response["access_token"]
        redis.set('sumup_token_info', json.dumps(response))
        redis.set('header_sumup', json.dumps({ 'Authorization': 'Bearer {}'.format(access_token) }) )
        return "Reconnected", 200
    else:
        print("You are not connected")
        return "You are not connected", 401

@connect_bp.route("/is_connected")
def is_connected():
    if redis.get('sumup_token_info') != '':
        token_info = json.loads(redis.get('sumup_token_info'))
        expires = datetime.datetime.fromtimestamp(token_info['expires_time'])
        if expires - datetime.timedelta(minutes=10) < datetime.datetime.now():
            redirect('reconnect')

        if json.loads(redis.get('header_sumup')):
            return { 'connected': True }, 200
    return { 'connected': False }, 200
    

@connect_bp.route("/get_client_id")
def get_client_id():
    return CLIENT_ID, 200

@connect_bp.route("/callback")
def callback():
    sumup_code = request.args.get("code")

    d = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": sumup_code
    }
    response = requests.post("https://api.sumup.com/token", data=d)
    if response.status_code != 200:
        return response.text, 500
    response = response.json()
    response['expires_time'] = (datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'] - 5)).timestamp()
    response['code'] = sumup_code
    access_token = response["access_token"]
    redis.set('sumup_token_info', json.dumps(response))
    redis.set('header_sumup', json.dumps({ 'Authorization': 'Bearer {}'.format(access_token) }) )

    redirect_url = redis.get('redirect_url')
    if redirect_url == '':
        redirect_url = '127.0.0.1:5000'
    print("redirecting to: " + redirect_url)
    return redirect(redirect_url)