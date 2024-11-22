import os
import requests
from typing import Optional, TypeVar, Dict, Any

# Generische Typen für die Eingabe- und Ausgabe-Datenmodelle
REQ = TypeVar('REQ')  # Request Model
RES = TypeVar('RES')  # Response Model

def api_fetch(path: str, token: str, method: str = 'GET', body: Optional[REQ] = None, headers: Optional[Dict[str, str]] = None) -> RES:
    """
    Führt eine API-Anfrage aus und gibt die Antwort zurück.
    """
    base_url = os.getenv("VREEDA_API_BASEURL", "https://api.example.com")  # Setze die Basis-URL aus Umgebungsvariablen
    url = f"{base_url}{path}"

    default_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Zusätzliche Header zusammenführen
    all_headers = {**default_headers, **(headers or {})}

    # Anfrage senden
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=all_headers,
            json=body  # `json` serialisiert das Body automatisch
        )

        # Fehlerbehandlung für HTTP-Fehler
        response.raise_for_status()

        # JSON-Antwort zurückgeben
        return response.json()  # Typ: RES
    except requests.HTTPError as http_err:
        try:
            # Versuche, eine detaillierte Fehlermeldung zu extrahieren
            error_detail = response.json().get("message", str(http_err))
        except Exception:
            error_detail = str(http_err)
        raise Exception(f"HTTP error! status: {response.status_code}, detail: {error_detail}") from http_err
    except Exception as err:
        raise Exception(f"An unexpected error occurred: {err}") from err

def list_devices(token: str) -> Dict[str, Any]:
    """
    Holt die Liste der Geräte aus der API.
    """
    return api_fetch('/1.0/Device', token, method='GET')

def patch_device(device_id: str, request: Dict[str, Any], token: str) -> Dict[str, Any]:
    """
    Aktualisiert ein Gerät in der API.
    """
    body = {device_id: request}
    return api_fetch(f'/1.0/Device/{device_id}', token, method='PATCH', body=body)