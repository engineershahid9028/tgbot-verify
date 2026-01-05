# engine/sheerid_engine.py

import asyncio

class SheerIDEngine:
    def __init__(self, client):
        self.client = client

    async def run_step(self, program_id, step, payload):
        code, data = await self.client.post_step(program_id, step, payload)
        if code != 200:
            raise Exception(f"SheerID step failed: {data}")
        return data

    async def poll_result(self, verification_id):
        while True:
            code, data = await self.client.get_status(verification_id)
            if data.get("status") in ("APPROVED", "DENIED"):
                return data
            await asyncio.sleep(3)
