# military/flow.py

from military.config import PROGRAM_ID
from military.utils import SheerIDClient
from military.engine.sheerid_engine import SheerIDEngine

class MilitaryVerifier:
    def __init__(self, token: str):
        self.client = SheerIDClient(token)
        self.engine = SheerIDEngine(self.client)

    async def verify(
        self,
        verification_id: str,
        first_name: str,
        last_name: str,
        email: str,
        dob: str,
        branch: str,
        status: str
    ):
        payload = {
            "firstName": first_name,
            "lastName": last_name,
            "email": email,
            "dateOfBirth": dob,
            "branchOfService": branch,
            "militaryStatus": status
        }

        await self.engine.run_step(
            PROGRAM_ID,
            "collectMilitaryPersonalInfo",
            payload
        )

        return await self.engine.poll_result(verification_id)

