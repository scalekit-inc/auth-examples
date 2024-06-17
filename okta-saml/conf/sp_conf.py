from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.saml import NAMEID_FORMAT_PERSISTENT


BASE_URL = "http://localhost:8443"

CONFIG = {
    'entityid': BASE_URL + '/saml/metadata/',
    'service': {
        'sp': {
            'name': 'SaaS Sample App',
            "name_id_policy_format": "urn:oasis:names:tc:SAML:2.0:nameid-format:persistent",
            'endpoints': {
                'assertion_consumer_service': [
                    (BASE_URL + '/saml/acs/', BINDING_HTTP_POST),
                ],
            },
            'allow_unsolicited': True,
            'authn_requests_signed': False,
            'want_assertions_signed': True,
            'want_response_signed': True,
        },
    },
    # Additional configurations ...
    'metadata': {
        'local': ['conf/idp-metadata.xml']
    }
    }

