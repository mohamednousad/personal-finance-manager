import requests
from config.settings import settings

class AuthService:
    def __init__(self):
        self.api_key = settings.FIREBASE_WEB_API_KEY
        self.base_url = "https://identitytoolkit.googleapis.com/v1/accounts"

    def signup(self, email, password):
        url = f"{self.base_url}:signUp?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Contains idToken, localId, etc.
        else:
            return {"error": response.json().get("error", {}).get("message", "Unknown error")}

    def signin(self, email, password):
        url = f"{self.base_url}:signInWithPassword?key={self.api_key}"
        payload = {
            "email": email,
            "password": password,
            "returnSecureToken": True
        }
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()  # Contains idToken, localId, etc.
        else:
            return {"error": response.json().get("error", {}).get("message", "Unknown error")}