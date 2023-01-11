# ########################################################################################################
#  Before giving feedback please note that I'm not sure what I'm doing here
#  I wanted just to create something which will ensure that my user is authenticated from vendor and
#  After that our proxy should be able to access vendor's tokens
#  We will then force the user to maintain their session over and over again until they have logged out
#  Author : Nasiruddin Saiyed
# #########################################################################################################

from flask import Flask, url_for, session, request
from flask import render_template, redirect
from authlib.integrations.requests_client import OAuth2Session

# App configuration
app = Flask(__name__)
app.secret_key = '!secret'
app.config.from_object('config')


# Configurations & Static Variables
# TODO: Load configuration from openid-configuration endpoint dynamically
# CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
ISSUER = ''
CONF_URL = ''
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_WEB_APP = ''


# OpenID Connect Client Config
AUTHORIZATION_ENDPOINT = ''
TOKEN_ENDPOINT = ''
REVOCATOPN_ENDPOINT = ''
SCOPE = ''
REDIRECT_URI = ''


# oauth = OAuth2Session(app)
oauth = OAuth2Session(
    # Request Client Authentication
    # refs :https://docs.authlib.org/en/latest/client/api.html
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorization_endpoint=AUTHORIZATION_ENDPOINT,
    token_endpoint=TOKEN_ENDPOINT,
    revocation_endpoint=REVOCATOPN_ENDPOINT,
    scope=SCOPE,
    redirect_uri=REDIRECT_URI
)

# Default landing page
# TODO: Dump it!
@app.route('/')
def homepage():
    user = session.get('user')
    return render_template('home.html', user=user)

# Implemented direct login for testing
# refs https://docs.authlib.org/en/latest/client/oauth2.html?highlight=grant_type%20password#oauth2session-for-password
# TODO: implement dynamic login via username and password
# TODO: again inject token data into oauth2 server & generate a new token
# TODO: Handle this with oauth2 server authentication 
@app.route('/login')
def login():
    # Configure the session with the client ID and secret
    session = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Fetch an access token
    url = TOKEN_ENDPOINT
    token = session.fetch_token(url, grant_type="password", username='', password='')

    print(token)
    return token


# Fetch client tokens
# refs https://docs.authlib.org/en/latest/client/oauth2.html?highlight=grant_type%20password#client-authentication
# TODO: again inject token data into oauth2 server & generate a new token
# TODO: Handle this with oauth2 server authentication 
@app.route('/client/login')
def clientLogin():
    # Configure the session with the client ID and secret
    session = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Fetch an access token
    url = TOKEN_ENDPOINT
    token = session.fetch_token(url, grant_type="client_credentials")

    print(token)
    return token

# Fetch new access token using refresh once its expired
# refs https://docs.authlib.org/en/latest/client/oauth2.html?highlight=grant_type%20password#refresh-auto-update-token
# TODO: again inject token data into oauth2 server & generate a new token
@app.route('/refresh')
def refresh():

    # Configure the session with the client ID and secret
    session = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Get token from query parameters
    refresh_token = request.args.get('refresh_token')

    # Fetch an access token
    url = TOKEN_ENDPOINT
    token = session.refresh_token(url, refresh_token=refresh_token)

    print(token)
    return token

# Remove user from current session & revoke access
# refs https://docs.authlib.org/en/latest/client/oauth2.html?highlight=grant_type%20password#revoke-and-introspect-token
# TODO: Handle this with oauth2 server authentication 
@app.route('/logout')
def logout():

    # Configure the session with the client ID and secret
    session = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Get token from auth header
    # headers = request.headers
    # bearer = headers.get('Authorization')    # Bearer YourTokenHere
    # authToken = bearer.split()[1]  # YourTokenHere

    # Get token from query parameters
    access_token = request.args.get('access_token')
    print(access_token)

    # Fetch an access token
    url = REVOCATOPN_ENDPOINT
    oauthResponse = session.revoke_token(url, token=access_token)
    
    print("REVOCATOPN_ENDPOINT >>>>> ", oauthResponse)
    return "Successfully kicked out!"
