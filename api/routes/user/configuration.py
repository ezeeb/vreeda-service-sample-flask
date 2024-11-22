from flask import jsonify, request, session, Blueprint
from api import mongo

blueprint = Blueprint('configuration', __name__)

@blueprint.route('/api/user/configuration', methods=['GET'])
def get_user_configuration():
    # Sitzung und Benutzer-ID überprüfen
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    if not user_id:
        return jsonify({"error": "User ID not found in session"}), 400

    try:
        # Benutzerkontext aus der Datenbank abrufen
        user_context = mongo.db.user_contexts.find_one({"user_id": user_id})
        if not user_context:
            return jsonify({"error": "User context not found"}), 404

        # Konfiguration zurückgeben oder leeres Objekt
        configuration = user_context.get("configuration", {})
        return jsonify(configuration), 200

    except Exception as e:
        print(f"Error fetching configuration: {e}")
        return jsonify({"error": "Failed to fetch configuration"}), 500


@blueprint.route('/api/user/configuration', methods=['POST'])
def update_user_configuration():
    # Sitzung und Benutzer-ID überprüfen
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session["user_id"]
    if not user_id:
        return jsonify({"error": "User ID not found in session"}), 400

    try:
        # JSON-Daten aus der Anfrage extrahieren
        body = request.get_json()
        configuration = body.get("configuration")

        if not configuration or not isinstance(configuration, dict):
            return jsonify({"error": "Invalid or missing configuration"}), 400

        # Benutzerkontext aktualisieren oder erstellen
        updated_context = mongo.db.user_contexts.find_one_and_update(
            {"user_id": user_id},
            {
                "$set": {"configuration": configuration},
                "$currentDate": {"updatedAt": True}
            },
            upsert=True,
            return_document=True  # Gibt das aktualisierte Dokument zurück
        )

        return jsonify(updated_context.get("configuration", {})), 200

    except Exception as e:
        print(f"Error updating configuration: {e}")
        return jsonify({"error": "Failed to update configuration"}), 500