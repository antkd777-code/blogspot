"""Blogger API OAuth2 인증 모듈 (리프레시 토큰 방식 — GitHub Actions 호환)"""
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import config


def get_blogger_service():
    token_url = "https://oauth2.googleapis.com/token"
    resp = requests.post(token_url, data={
        "client_id": config.GOOGLE_CLIENT_ID,
        "client_secret": config.GOOGLE_CLIENT_SECRET,
        "refresh_token": config.GOOGLE_REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    resp.raise_for_status()
    access_token = resp.json()["access_token"]

    creds = Credentials(
        token=access_token,
        refresh_token=config.GOOGLE_REFRESH_TOKEN,
        token_uri=token_url,
        client_id=config.GOOGLE_CLIENT_ID,
        client_secret=config.GOOGLE_CLIENT_SECRET,
    )
    return build("blogger", "v3", credentials=creds)
