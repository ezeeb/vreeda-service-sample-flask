from flask import Blueprint, session, jsonify
from datetime import timedelta

blueprint = Blueprint('session', __name__)

@blueprint.route('/api/auth/session')
def api_session():
    if "user_id" not in session:
        return jsonify({"logged_in": False})

    return jsonify({
        "loggedIn": True,
        "user": {
            "id": session.get('user_id'),
            "name": session.get('name'),
            "email": session.get('email')
        }
    })