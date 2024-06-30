import os
import json
from flask import Flask, url_for, session, redirect, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)


appConf = {
    "OAUTH2_CLIENT_ID": os.environ.get("OAUTH2_CLIENT_ID"),
    "OAUTH2_CLIENT_SECRET": os.environ.get("OAUTH2_CLIENT_SECRET"),
    "OAUTH_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": os.environ.get("FLASK_SECRET"),
    "FLASK_PORT": 5000
}

app.secret_key = appConf.get("FLASK_SECRET")

oauth = OAuth(app)
oauth.register("DorfakSoftApp",
               client_id=appConf.get("OAUTH2_CLIENT_ID"),
               client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
               server_metadata_url=appConf.get("OAUTH_META_URL"),
               client_kwargs={
                   "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read", }
               )


@app.route("/")
def home():
    return render_template("home.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"), indent=4))


@app.route("/google-login")
def google_login():
    return oauth.DorfakSoftApp.authorize_redirect(redirect_uri=url_for("google_callback", _external=True))


@app.route("/signin-google")
def google_callback():
    token = oauth.DorfakSoftApp.authorize_access_token()
    session["user"] = token
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
