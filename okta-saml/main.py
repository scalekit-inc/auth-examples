from flask import Flask, request, redirect, url_for, make_response, session
from markupsafe import escape
from saml2 import entity
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from conf.sp_conf import CONFIG, BASE_URL
from xml.etree import ElementTree
from saml2 import BINDING_HTTP_POST, BINDING_HTTP_REDIRECT
from pprint import pprint
from saml2.saml import NAMEID_FORMAT_PERSISTENT, NameID
from saml2.metadata import entity_descriptor
from flask import render_template
import os
import base64
import argparse

# Define the argument parser and parse arguments
parser = argparse.ArgumentParser(description='Sample SaaS App')
parser.add_argument('--debug', action='store_true', help='Enable debug mode')
args = parser.parse_args()

# Function to handle logging
def debug_log(message):
    """
    Pprint log and error messages if the --debug argument
    is present on the command line.

    Args:
        message (str): informative message

    Returns:
        None
    """
    if args.debug:
        pprint(message)


def saml_client_for(config):
    """
    Create a SAML client using the provided configuration.

    Args:
        config (str): Path to the SAML configuration file.

    Returns:
        Saml2Client: A SAML client instance.

    """
    conf = Saml2Config()
    conf.load(config)
    return Saml2Client(conf)

app = Flask(__name__)

# Register the format_xml_filter with the Jinja environment

# Set the secret key to some random bytes. Keep this really secret!
# This enables Flask session cookies
app.secret_key = os.urandom(24)

@app.route("/")
def hello():
    """
    Displays a welcome message and user information if the user is authenticated,
    otherwise displays a login link.
    Returns:
    tuple: A tuple containing the HTML content and the HTTP status code.
    """
    # Check if user is authenticated
    is_authenticated = session.get('is_authenticated', False)

    if is_authenticated:
        name_id = escape(session.get('name_id', ''))
        first_name = escape(session.get('firstname', ''))
        last_name = escape(session.get('lastname', ''))
        email = escape(session.get('email', ''))
        profileUrl = escape(session.get('profileUrl', ''))
        authn_response_string = session.get('authn_response_string', '')
        attributes = session.get('attributes','{}')

        return render_template('template.html', is_authenticated=is_authenticated,
                                name_id=name_id, first_name=first_name,
                                last_name=last_name, email=email,
                                authn_response_string=authn_response_string,
                                profileUrl=profileUrl,
                                attributes=attributes), 200
    else:
        metadata_url = BASE_URL + "/saml/metadata"

        return render_template('template.html',
                                is_authenticated=is_authenticated,
                                metadata_url=metadata_url), 200


@app.route('/login')
def login():
    """
    Initiates the SAML authentication process by creating an authentication request and redirecting the user to the IdP's login page.

    Returns:
        If the redirect URL is available, the function redirects the user to the IdP's login page.
        If the redirect URL is not available, the function returns an error message with status code 500.
    """
    client = saml_client_for(CONFIG)

    # Create the SAML authentication request
    (session_id, result) = client.prepare_for_authenticate()

    # Redirect the user to the IdP's login page
    redirect_url = None
    for key, value in result['headers']:
        if key == 'Location':
            redirect_url = value
            break

    if redirect_url:
        return redirect(redirect_url)
    else:
        return "Error: Couldn't redirect to IdP for login.", 500


@app.route('/saml/acs/', methods=['POST'])
def acs():
    """
    Process the SAML Assertion Consumer Service (ACS) request.

    This function handles the SAML response received from the Identity Provider (IdP) after the user
    has been authenticated. It extracts the user's attributes from the SAML response, sets the user
    session, and redirects the user to the 'hello' endpoint.

    Returns:
        A redirect response to the 'hello' endpoint if the SAML response is successfully processed.
        An error message with status code 500 if there is an exception during processing.
    """
    client = saml_client_for(CONFIG)
    try:
        # Parse the SAML Response

        saml_response = request.form.get('SAMLResponse')
        authn_response = client.parse_authn_request_response(saml_response, entity.BINDING_HTTP_POST)

        debug_log(f"authn_response.status_ok(): {authn_response.status_ok()}")
        # Extract the user's NameID and attributes
        name_id = authn_response.assertion.subject.name_id.text
        debug_log(f"name_id: {name_id}")

        # Accessing attributes directly from the assertion
        attributes = {}
        for statement in authn_response.assertion.attribute_statement:
            for attribute in statement.attribute:
                # Assuming single value attributes for simplicity
                attributes[attribute.name] = attribute.attribute_value[0].text


         # Convert authn_response object to string
        authn_response_string = str(authn_response)

        # Store authn_response string in session
        session['authn_response_string'] = authn_response_string


        # Set the user session
        session['name_id'] = name_id
        session['firstname'] = attributes.get('firstname', None)
        session['lastname'] = attributes.get('lastname', None)
        session['is_authenticated'] = True
        session['email'] = attributes.get('email', None)
        session['profileUrl']= attributes.get('profileUrl',None)
        session['attributes'] = attributes

        return redirect(url_for('hello'))

    except Exception as e:
        # Log the exception for debugging
        debug_log(f"SAML ACS Error: {e}")

        # Clear any existing session and display error
        session.clear()
        return f"EXCEPTION {e}", 403

@app.route('/logout')
def logout():
    """
    Clear the current session.
    """
    
    session.clear()
    return redirect(url_for('hello'))

@app.route('/saml/metadata/')
def metadata():
    """
    Generates the metadata for the SAML service provider.

    Returns:
        flask.Response: The metadata XML response.
    """
    conf = Saml2Config()
    conf.load(CONFIG)
    metadata_content = entity_descriptor(conf).to_string()
    response = make_response(metadata_content, 200)
    response.headers['Content-Type'] = 'application/xml'
    return response

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8443)

