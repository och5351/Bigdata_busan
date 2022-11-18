from flask import Blueprint, Flask, abort, redirect, request, session, url_for

from google_auth_oauthlib.flow import Flow
import os, pathlib
from pip._vendor import cachecontrol
import google.auth.transport.requests
from google.oauth2 import id_token
import requests

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# 구글 Oauth 설정
GOOGLE_CLIENT_ID = "167648320999-47vq0ttrba3igorui2h372vhjbqcnp89.apps.googleusercontent.com"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "C:\localRepository\Bigdata_busan\ldg\project\dogma\static\client_secret.json")
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "../static/client_secret.json")
# 서버 파일 경로
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "/home/ubuntu/projects/Bigdata_busan/ldg/project/dogma/static/client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/oauth/callback"
    )

bp = Blueprint("oauth", __name__, url_prefix="/oauth")

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401) # Authorization required
        else:
            return function()
    return wrapper

@bp.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@bp.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) # state does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID,
        clock_skew_in_seconds=2
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect(url_for('main.main'))

@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@bp.route("/protected_area")
@login_is_required
def protected_area():
    return "protected! <a href='/oauth/logout'><button>Logout</button></a>"