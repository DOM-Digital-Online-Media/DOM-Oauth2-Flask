# OAuth2 Direct login demo with Flask

You can learn Flask OAuth 2.0 client with this demo.

## Install

Install the required dependencies:

    $ pip install -U Flask Authlib requests

## Run

Start server with:

    $ export FLASK_APP=app.py
    $ flask run

Then visit:

    http://127.0.0.1:5000/


## Mile Stone 
1. Create a oauth2 client which will authenticate on behalf of the user with vendor authentication
2. Create a new oauth2 server which will force encryption on vendor authentication payload & provide protection against accessing api. Proxy will be allowed to decode credentials
3. Configure client to connect and load configuration from issuer. 
4. Create a new oauth2 client which will authenticate in between proxied and frontend requests.