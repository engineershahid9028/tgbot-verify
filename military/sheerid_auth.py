# sheerid_auth.py
import time
import threading
import requests
from typing import Optional


class SheerIDTokenManager:
    def __init__(self, client_id: str, client_secret: str, auth_url: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_url = auth_url

        self._token: Optional[str] = None
        self._expires_at: float = 0.0
        self._lock = threading.Lock()

    def _fetch_token(self):
        r = requests.post(
            self.auth_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
            timeout=20,
        )
        r.raise_for_status()
        data = r.json()
        self._token = data["access_token"]
        # refresh 60s early
        self._expires_at = time.time() + int(data.get("expires_in", 3600)) - 60

    def get_token(self) -> str:
        with self._lock:
            if not self._token or time.time() >= self._expires_at:
                self._fetch_token()
            return self._token
