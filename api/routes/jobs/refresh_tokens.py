from flask import jsonify, request, Blueprint
import os
import requests
from datetime import datetime, timedelta
from api import mongo

blueprint = Blueprint('refresh-tokens', __name__)

# Azure AD B2C Konfiguration aus Umgebungsvariablen
AZURE_AD_B2C_TENANT_NAME = os.getenv("AZURE_AD_B2C_TENANT_NAME")
AZURE_AD_B2C_PRIMARY_USER_FLOW = os.getenv("AZURE_AD_B2C_PRIMARY_USER_FLOW")
AZURE_AD_B2C_CLIENT_ID = os.getenv("AZURE_AD_B2C_CLIENT_ID")
AZURE_AD_B2C_CLIENT_SECRET = os.getenv("AZURE_AD_B2C_CLIENT_SECRET")
API_REFRESH_TOKENS_JOB_KEY = os.getenv("API_REFRESH_TOKENS_JOB_KEY")

@blueprint.route('/api/jobs/refresh-tokens', methods=['GET'])
def refresh_tokens():

    api_key = request.args.get("key")
    if api_key != API_REFRESH_TOKENS_JOB_KEY:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    try:
        threshold = datetime.utcnow() + timedelta(minutes=5)

        print(f"Token refresh job: checking for access token expiration before {threshold.isoformat()}")

        users_to_refresh = mongo.db.user_contexts.find({
            "api_access_tokens.access_token_expiration": {"$lt": threshold}
        })

        for user in users_to_refresh:
            try:
                refresh_token = user.get("api_access_tokens", {}).get("refresh_token")
                if not refresh_token:
                    print(f"Skipping user {user['user_id']} due to missing refresh token.")
                    continue

                token_url = f"https://{AZURE_AD_B2C_TENANT_NAME}.b2clogin.com/{AZURE_AD_B2C_TENANT_NAME}.onmicrosoft.com/{AZURE_AD_B2C_PRIMARY_USER_FLOW}/oauth2/v2.0/token"
                response = requests.post(
                    token_url,
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                    data={
                        "client_id": AZURE_AD_B2C_CLIENT_ID,
                        "client_secret": AZURE_AD_B2C_CLIENT_SECRET,
                        "grant_type": "refresh_token",
                        "refresh_token": refresh_token,
                    },
                )

                if response.status_code != 200:
                    print(f"Failed to refresh token for user {user['user_id']}: {response.text}")
                    continue

                data = response.json()

                mongo.db.user_contexts.update_one(
                    {"_id": user["_id"]},
                    {
                        "$set": {
                            "api_access_tokens.access_token": data["access_token"],
                            "api_access_tokens.refresh_token": data.get("refresh_token", refresh_token),
                            "api_access_tokens.access_token_expiration": datetime.utcnow() + timedelta(seconds=data["expires_in"]),
                            "api_access_tokens.refresh_token_expiration": datetime.utcnow() + timedelta(seconds=data["refresh_token_expires_in"]),
                        },
                        "$currentDate": {"updated_at": True}
                    }
                )

                print(f"Successfully refreshed token for user {user['user_id']}")
            except Exception as e:
                print(f"Error refreshing token for user {user['user_id']}: {e}")

        print("Token refresh job: completed successfully.")
        return jsonify({"success": True, "message": "Token refresh completed successfully."})
    except Exception as e:
        print(f"Error in token refresh job: {e}")
        return jsonify({"success": False, "message": "Failed to refresh tokens."}), 500
