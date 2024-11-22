from flask import Blueprint, session, jsonify
from datetime import datetime
from api import mongo

blueprint = Blueprint('granted', __name__)

@blueprint.route('/api/user/granted')
def api_granted():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    users_collection = mongo.db.user_contexts
    user_context = users_collection.find_one({"user_id": user_id})
    if not user_context:
        return jsonify({"granted": False, "message": "User context not found"}), 404

    api_access_tokens = user_context.get("api_access_tokens", {})
    access_token = api_access_tokens.get("access_token")
    refresh_token = api_access_tokens.get("refresh_token")
    access_token_expiration = api_access_tokens.get("access_token_expiration")
    refresh_token_expiration = api_access_tokens.get("refresh_token_expiration")

    if not access_token or not refresh_token:
        return jsonify({"granted": False, "message": "Tokens are missing"}), 401

    now = datetime.utcnow()

    if isinstance(access_token_expiration, str):
        access_token_expiration = datetime.fromisoformat(access_token_expiration)

    if isinstance(refresh_token_expiration, str):
        refresh_token_expiration = datetime.fromisoformat(refresh_token_expiration)

    access_token_expired = access_token_expiration and access_token_expiration <= now
    refresh_token_expired = refresh_token_expiration and refresh_token_expiration <= now

    if access_token_expired or refresh_token_expired:
        return jsonify({"granted": False, "message": "Tokens are expired"}), 401
    
    return jsonify({"granted": True, "message": "Access granted"}), 200