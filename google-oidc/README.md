# Google OIDC Login Demo App

This is an app to understand how to configure Google OIDC for login. This is built using Python and Flask using [AuthLib](https://authlib.org/).

## Install

Install the required dependencies:

    $ pip install -U Flask Authlib requests

## Config

1. Create a [Google Developer Account](https://developers.google.com) if you don't already have one.
2. Create a new Google Project
3. Configure the OAuth Consent Screen:
   1. In the Cloud Console, go to APIs & Services > OAuth consent screen.
   2. Choose "External" and click "Create".
   3. Fill out the form with required details (e.g., App name, User support email).
   4. Add scopes `email`, `openid` and `profile`.
   5. Save and continue.
4. Create your Google OAuth Credentials:
   1. In the Cloud Console, go to APIs & Services > Credentials.
   2. Click "Create Credentials" and select "OAuth 2.0 Client ID".
   3. Select "Web application".
   4. Enter a name for the credential.
   5. Under "Authorized redirect URIs", add the URI where Google will redirect after the user authenticates, in this case `http://127.0.0.1:5000/authorize`
5. Save Your Client ID and Client Secret.

Fill the given client ID and secret into `config.py`.

## Run

Start server with:

    $ export FLASK_APP=app.py
    $ flask run

Then visit:

    http://127.0.0.1:5000/