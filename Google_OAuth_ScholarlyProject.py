from flask import Flask, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_dance.consumer import oauth_authorized
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #env variable needed for local use to allow oauth to be served over HTTP instead of HTTPS
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1' #google has a tendency to return different OAuth scopes that causes an error; this stops that from happening

app = Flask(__name__)
app.secret_key = "suuupersecret"
google_blueprint = make_google_blueprint( #blueprint for google oauth; most providers require client_id and client_secret while providing other optional paramters
    client_id="CLIENT_ID", #generated via google cloud console, typically placed in a config file as GOOGLE_OAUTH_CLIENT_ID
    client_secret="CLIENT_SECRET", #generated via google cloud console, typically placed in a config file as GOOGLE_OAUTH_CLIENT_SECRET
    scope=["profile", "email"] #limits applications access to a users account; in this case we can access their profile and email
)
app.register_blueprint(google_blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    response = google_blueprint.session.get("/oauth2/v2/userinfo")
    if response.ok:
        userInfo = response.json()
        #idToken= google.token["id_token"] --> Needs to be decoded
        return userInfo
    return "???"

if __name__ == "__main__":
    app.run()
    