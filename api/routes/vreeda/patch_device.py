from libs.vreeda_api_client import patch_device
from flask import Blueprint, session, jsonify, request
from api import mongo

blueprint = Blueprint('patch-device', __name__)

@blueprint.route('/api/vreeda/patch-device', methods=['PATCH'])
def api_patch_device():

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
        request_data = request.get_json()
        device_id = request_data.get("deviceId")
        patch_request = request_data.get("request")
    except Exception:
        return jsonify({"error": "Invalid JSON body"}), 400

    if not device_id or not patch_request:
        return jsonify({"error": "Missing deviceId or request body"}), 400

    try:
        updated_device = patch_device(device_id, patch_request, access_token)
        return jsonify(updated_device), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500