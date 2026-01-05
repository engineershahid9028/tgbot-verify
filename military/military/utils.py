# military/utils.py

import httpx

class SheerIDClient:
    def __init__(self, token: str):
        self.base_url = "https://services.sheerid.com/rest/v2/verification"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

    async def post_step(self, program_id: str, step: str, payload: dict):
        url = f"{self.base_url}/{program_id}/step/{step}"
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(url, json=payload, headers=self.headers)
            return r.status_code, r.json()

    async def get_status(self, verification_id: str):
        url = f"{self.base_url}/{verification_id}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self.headers)
            return r.status_code, r.json()
