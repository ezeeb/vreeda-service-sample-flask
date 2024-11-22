from flask import Blueprint, session, redirect
import os
from datetime import timedelta

blueprint = Blueprint('logout', __name__)

TENANT_NAME = os.getenv('AZURE_AD_B2C_TENANT_NAME')
CLIENT_ID = os.getenv('AZURE_AD_B2C_CLIENT_ID')
HOST_URL = os.getenv('HOST_URL')
REDIRECT_URI = f"{HOST_URL}/"
POLICY = os.getenv('AZURE_AD_B2C_PRIMARY_USER_FLOW')
AUTHORITY = f"https://{TENANT_NAME}.b2clogin.com/{TENANT_NAME}.onmicrosoft.com/{POLICY}"

@blueprint.route('/api/auth/logout')
def api_logout():

    session.clear()

    logout_url = f"{AUTHORITY}/oauth2/v2.0/logout?post_logout_redirect_uri={REDIRECT_URI}"
    return redirect(logout_url)