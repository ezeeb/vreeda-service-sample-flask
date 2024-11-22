from flask import Blueprint, request, session, redirect
import requests
import os
from datetime import timedelta
from jose import jwt
import datetime
from api import mongo

blueprint = Blueprint('callback', __name__)

TENANT_NAME = os.getenv('AZURE_AD_B2C_TENANT_NAME')
CLIENT_ID = os.getenv('AZURE_AD_B2C_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_AD_B2C_CLIENT_SECRET')
HOST_URL = os.getenv('HOST_URL')
REDIRECT_URI = f"{HOST_URL}/api/auth/callback/azure-ad-b2c"
POLICY = os.getenv('AZURE_AD_B2C_PRIMARY_USER_FLOW')
AUTHORITY = f"https://{TENANT_NAME}.b2clogin.com/{TENANT_NAME}.onmicrosoft.com/{POLICY}"

SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', 30))  # Timeout in Minuten

@blueprint.route('/api/auth/callback/azure-ad-b2c')
def api_auth_callback():

    code = request.args.get('code')
    if not code:
        return "Authorization code not found.", 400

    token_url = f"{AUTHORITY}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }
    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        joresponse = response.json()

        decoded_access_token = jwt.get_unverified_claims(joresponse.get('access_token'))
        user_id = decoded_access_token.get('sub')

        session.permanent = True
        blueprint.permanent_session_lifetime = timedelta(minutes=SESSION_TIMEOUT)
        session['access_token'] = joresponse.get('access_token')
        session['user_id'] = user_id
        session['name'] = decoded_access_token.get('name')
        session['email'] = decoded_access_token.get('email')

        user_data = {
            "user_id": user_id,
            "api_access_tokens": {
                "access_token": joresponse.get('access_token'),
                "refresh_token": joresponse.get('refresh_token'),
                "access_token_expiration": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(joresponse.get('expires_in', 3600))),
                "refresh_token_expiration": datetime.datetime.utcnow() + datetime.timedelta(seconds=int(joresponse.get('refresh_token_expires_in', 0))),
            },
            "configuration": {},
            "created_at": datetime.datetime.utcnow(),
            "updated_at": datetime.datetime.utcnow()
        }

        users_collection = mongo.db.user_contexts

        existing_user = users_collection.find_one({"user_id": user_id})
        if existing_user:
            users_collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": {
                    "api_access_tokens": user_data["api_access_tokens"],
                    "updated_at": datetime.datetime.utcnow()
                }}
            )
        else:
            users_collection.insert_one(user_data)

        return redirect('/')
    else:
        return f"Failed to obtain tokens: {response.text}", response.status_code
