import time
import requests
from django.conf import settings

_TOKEN = None
_TOKEN_EXPIRES = 0

def _refresh_token():
    global _TOKEN, _TOKEN_EXPIRES
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
      'client_id': settings.IGDB_CLIENT_ID,
      'client_secret': settings.IGDB_CLIENT_SECRET,
      'grant_type': 'client_credentials'
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    _TOKEN = data['access_token']
    # Ajusta un margen antes de la expiración real
    _TOKEN_EXPIRES = time.time() + data['expires_in'] - 60

def _get_token():
    if not _TOKEN or time.time() >= _TOKEN_EXPIRES:
        _refresh_token()
    return _TOKEN

def igdb_request(endpoint: str, query: str):
    """
    Hace una petición POST a https://api.igdb.com/v4/{endpoint}
    con cuerpo en lenguaje IGDB y devuelve la lista de resultados.
    """
    token = _get_token()
    headers = {
      'Client-ID': settings.IGDB_CLIENT_ID,
      'Authorization': f'Bearer {token}'
    }
    url = f'https://api.igdb.com/v4/{endpoint}'
    resp = requests.post(url, headers=headers, data=query)
    resp.raise_for_status()
    return resp.json()
