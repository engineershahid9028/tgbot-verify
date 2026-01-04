"""
SheerID 教师验证主程序（最终稳定版）
"""

import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple

try:
    from . import config
    from .name_generator import NameGenerator, generate_email, generate_birth_date
    from .img_generator import generate_teacher_pdf, generate_teacher_png
except ImportError:
    import config
    from name_generator import NameGenerator, generate_email, generate_birth_date
    from img_generator import generate_teacher_pdf, generate_teacher_png


PROGRAM_ID = config.PROGRAM_ID
SHEERID_BASE_URL = config.SHEERID_BASE_URL
SCHOOLS = config.SCHOOLS
DEFAULT_SCHOOL_ID = config.DEFAULT_SCHOOL_ID


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:

    def __init__(self, verification_id: str):
        self.verification_id = verification_id
        self.device_fingerprint = self._gen_device_fingerprint()
        self.client = httpx.Client(timeout=30.0)

    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass

    # ---------- helpers ----------

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        if not url:
            return None
        m = re.search(r"verificationId=([a-f0-9]+)", url, re.IGNORECASE)
        return m.group(1) if m else None

    @staticmethod
    def _gen_device_fingerprint() -> str:
        return "".join(random.choice("0123456789abcdef") for _ in range(32))

    def _request(self, method: str, url: str, body: Dict = None) -> Tuple[Dict, int]:
        r = self.client.request(
            method=method,
            url=url,
            json=body,
            headers={"Content-Type": "application/json"}
        )
        try:
            data = r.json()
        except Exception:
            data = {}
        return data, r.status_code

    def _get_current_step(self) -> str:
        data, status = self._request(
            "GET",
            f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}"
        )
        if status != 200:
            raise Exception(data)
        return data.get("currentStep")

    def _upload(self, url: str, content: bytes, mime: str) -> bool:
        r = self.client.put(
            url,
            content=content,
            headers={"Content-Type": mime},
            timeout=60.0
        )
        return 200 <= r.status_code < 300

    # ---------- main flow ----------

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        school_id: str = None
    ) -> Dict:

        if not first_name or not last_name:
            name = NameGenerator.generate()
            first_name = name["first_name"]
            last_name = name["last_name"]

        email = email or generate_email(first_name, last_name)
        birth_date = birth_date or generate_birth_date()

        school_id = school_id or DEFAULT_SCHOOL_ID
        school = SCHOOLS[school_id]

        logger.info(f"教师信息: {first_name} {last_name}")
        logger.info(f"邮箱: {email}")
        logger.info(f"学校: {school['name']}")
        logger.info(f"生日: {birth_date}")
        logger.info(f"验证ID: {self.verification_id}")

        pdf_data = generate_teacher_pdf(first_name, last_name)
        png_data = generate_teacher_png(first_name, last_name)

        pdf_size = len(pdf_data)
        png_size = len(png_data)

        # ---- step routing ----
        while True:
            step = self._get_current_step()
            logger.info(f"当前 SheerID 步骤: {step}")

            if step == "collectPersonalInfo":
                body = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "birthDate": birth_date,
                    "email": email,
                    "phoneNumber": "",
                    "deviceFingerprintHash": self.device_fingerprint,
                    "locale": "en-US",
                    "metadata": {
                        "verificationId": self.verification_id
                    }
                }
                data, status = self._request(
                    "POST",
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectPersonalInfo",
                    body
                )
                if status != 200:
                    raise Exception(data)
                continue

            if step == "collectTeacherPersonalInfo":
                # ✅ CORRECTED PAYLOAD (NO employmentStatus)
                body = {
                    "firstName": first_name,
                    "lastName": last_name,
                    "birthDate": birth_date,
                    "email": email,
                    "organization": {
                        "id": school["id"],
                        "idExtended": school["idExtended"],
                        "name": school["name"]
                    },
                    "deviceFingerprintHash": self.device_fingerprint,
                    "locale": "en-US",
                    "metadata": {
                        "verificationId": self.verification_id
                    }
                }
                data, status = self._request(
                    "POST",
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
                    body
                )
                if status != 200:
                    raise Exception(data)
                continue

            if step == "sso":
                self._request(
                    "DELETE",
                    f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                )
                continue

            if step == "docUpload":
                break

            if step in ("pending", "approved"):
                return {
                    "success": True,
                    "pending": step == "pending",
                    "verification_id": self.verification_id
                }

            if step == "error":
                raise Exception("SheerID error state")

        # ---- document upload ----
        body = {
            "files": [
                {"fileName": "teacher.pdf", "mimeType": "application/pdf", "fileSize": pdf_size},
                {"fileName": "teacher.png", "mimeType": "image/png", "fileSize": png_size}
            ]
        }

        data, status = self._request(
            "POST",
            f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/docUpload",
            body
        )
        if status != 200:
            raise Exception("docUpload failed")

        pdf_url = data["documents"][0]["uploadUrl"]
        png_url = data["documents"][1]["uploadUrl"]

        if not self._upload(pdf_url, pdf_data, "application/pdf"):
            raise Exception("PDF upload failed")
        if not self._upload(png_url, png_data, "image/png"):
            raise Exception("PNG upload failed")

        self._request(
            "POST",
            f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/completeDocUpload"
        )

        return {
            "success": True,
            "pending": True,
            "verification_id": self.verification_id,
            "message": "文档已提交，等待审核"
        }
