from libs.vreeda_api_client import list_devices
from flask import Blueprint, session, jsonify
from api import mongo

blueprint = Blueprint('list-devices', __name__)

@blueprint.route('/api/vreeda/list-devices', methods=['GET'])
def api_list_devices():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]

    users_collection = mongo.db.user_contexts
    user_context = users_collection.find_one({"user_id": user_id})
    if not user_context:
        return jsonify({"granted": False, "message": "User context not found"}), 404

    api_access_tokens = user_context.get("api_access_tokens", {})
    access_token = api_access_tokens.get("access_token")

    if not access_token:
        return jsonify({"granted": False, "message": "Tokens are missing"}), 401

    try:
        devices = list_devices(access_token)
        return jsonify(devices)
    except Exception as e:
        return jsonify({"error": str(e)}), 500