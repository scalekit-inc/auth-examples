# SAML2.0 Demo with Okta - Python Application

This is an app to understand how to configure Okta SAML for login. This is built using Python and Flask using [pysaml2](https://github.com/IdentityPython/pysaml2).

## Prerequisites

- Python 3.x
- Flask
- pysaml2
- Okta Developer Account

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/scalekit-inc/auth-examples.git
   cd okta-saml
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create Okta Account, and follow [these steps](https://help.okta.com/en-us/content/topics/apps/apps_app_integration_wizard_saml.htm) to register the application and get the metadata file. 
2. Place your IdP metadata in this location `conf/idp-metadata.xml`


## Running the Application

1. Run the Flask application:

   ```bash
   python main.py
   ```

2. Access the application at `https://localhost:8443`

## Enabling Debug Mode

```bash
python main.py --debug
```

