import requests
from rest_framework.utils import json
from django.conf import settings

def get_access_token(AUTH0_DOMAIN, AUTH0_AUDIENCE, CLIENT_ID, CLIENT_SECRET):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    raw_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "audience": AUTH0_AUDIENCE,
        "grant_type": settings.GRANT_TYPE
    }
    auth_token_response = requests.post(
        url,
        data=json.dumps(raw_data),
        headers={"Content-Type": "application/json"},
    )
    if auth_token_response.status_code == 200:
        response_data = auth_token_response.json()
        return response_data.get('access_token')
    return None
