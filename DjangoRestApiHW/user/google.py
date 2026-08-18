import requests

from django.conf import settings


def get_google_tokens(code):
    url = "https://oauth2.googleapis.com/token"

    data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": "http://127.0.0.1:8000/api/v1/auth/google/callback/",
        "grant_type": "authorization_code",
    }

    response = requests.post(url, data=data)

    return response.json()


def get_google_user(access_token):
    url = "https://www.googleapis.com/oauth2/v3/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)

    return response.json()
