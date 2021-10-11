from flask import Blueprint
from flask import redirect, request, url_for

from app import CLIENT_ID, redis

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
    

@connect_bp.route("/get_client_id")
def get_client_id():
    return CLIENT_ID, 200

@connect_bp.route("/callback")
def callback():
    sumup_code = request.args.get("code")
    return redirect(url_for("transactions.fetch_all_transactions", sumup_code=sumup_code))