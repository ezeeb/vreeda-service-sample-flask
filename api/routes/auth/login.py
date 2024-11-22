from flask import Blueprint, redirect
import os

blueprint = Blueprint('login', __name__)

TENANT_NAME = os.getenv('AZURE_AD_B2C_TENANT_NAME')
CLIENT_ID = os.getenv('AZURE_AD_B2C_CLIENT_ID')
HOST_URL = os.getenv('HOST_URL')
REDIRECT_URI = f"{HOST_URL}/api/auth/callback/azure-ad-b2c"
POLICY = os.getenv('AZURE_AD_B2C_PRIMARY_USER_FLOW')
AUTHORITY = f"https://{TENANT_NAME}.b2clogin.com/{TENANT_NAME}.onmicrosoft.com/{POLICY}"

@blueprint.route('/api/auth/login')
def api_login():
    authorization_url = (
        f"{AUTHORITY}/oauth2/v2.0/authorize?"
        f"client_id={CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={REDIRECT_URI}&"
        f"response_mode=query&"
        f"scope={CLIENT_ID} offline_access openid&"
        f"state=12345"
    )
    return redirect(authorization_url)