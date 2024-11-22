from flask import Blueprint, session, jsonify
from api import mongo

blueprint = Blueprint('revoke', __name__)

@blueprint.route('/api/user/revoke', methods=['DELETE'])
def revoke_user():

    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User ID not found in session"}), 400

    try:

        result = mongo.db.user_contexts.delete_one({"user_id": user_id})

        if result.deleted_count == 0:
            return jsonify({"error": "User context not found"}), 404

        # Optional: Logout auslösen, z. B. durch Leeren der Sitzung
        session.clear()

        return jsonify({"message": "User revoked and logged out"}), 200

    except Exception as e:
        print(f"Error revoking user: {e}")
        return jsonify({"error": "Failed to revoke user"}), 500