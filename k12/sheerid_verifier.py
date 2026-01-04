"""SheerID 教师验证主程序（完整稳定版）"""

import re
import random
import logging
import httpx
from typing import Dict, Optional, Tuple

# 兼容包 / 脚本运行
try:
    from . import config  # type: ignore
    from .name_generator import NameGenerator, generate_email, generate_birth_date  # type: ignore
    from .img_generator import generate_teacher_pdf, generate_teacher_png  # type: ignore
except ImportError:
    import config  # type: ignore
    from name_generator import NameGenerator, generate_email, generate_birth_date  # type: ignore
    from img_generator import generate_teacher_pdf, generate_teacher_png  # type: ignore


# 配置
PROGRAM_ID = config.PROGRAM_ID
SHEERID_BASE_URL = config.SHEERID_BASE_URL
SCHOOLS = config.SCHOOLS
DEFAULT_SCHOOL_ID = config.DEFAULT_SCHOOL_ID


# 日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class SheerIDVerifier:
    """SheerID 教师身份验证器（完整类）"""

    def __init__(self, verification_id: str):
        self.verification_id = verification_id
        self.device_fingerprint = self._gen_device_fingerprint()
        self.client = httpx.Client(timeout=30.0)

    def __del__(self):
        try:
            self.client.close()
        except Exception:
            pass

    # -------------------------
    # 工具方法
    # -------------------------

    @staticmethod
    def parse_verification_id(url: str) -> Optional[str]:
        """从 URL 中解析 verificationId"""
        if not url:
            return None
        match = re.search(r'verificationId=([a-f0-9]+)', url, re.IGNORECASE)
        return match.group(1) if match else None

    @staticmethod
    def _gen_device_fingerprint() -> str:
        return ''.join(random.choice('0123456789abcdef') for _ in range(32))

    def _request(self, method: str, url: str, body: Dict = None) -> Tuple[Dict, int]:
        response = self.client.request(
            method=method,
            url=url,
            json=body,
            headers={"Content-Type": "application/json"}
        )
        try:
            data = response.json()
        except Exception:
            data = {}
        return data, response.status_code

    def _get_current_step(self) -> str:
        data, status = self._request(
            "GET",
            f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}"
        )
        if status != 200:
            raise Exception(f"获取验证状态失败: {data}")
        return data.get("currentStep")

    def _upload(self, url: str, content: bytes, mime: str) -> bool:
        response = self.client.put(
            url,
            content=content,
            headers={"Content-Type": mime},
            timeout=60.0
        )
        return 200 <= response.status_code < 300

    # -------------------------
    # 主验证流程
    # -------------------------

    def verify(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        birth_date: str = None,
        school_id: str = None
    ) -> Dict:

        try:
            # 基础信息
            if not first_name or not last_name:
                name = NameGenerator.generate()
                first_name = name["first_name"]
                last_name = name["last_name"]

            email = email or generate_email()
            birth_date = birth_date or generate_birth_date()

            school_id = school_id or DEFAULT_SCHOOL_ID
            school = SCHOOLS[school_id]

            logger.info(f"教师信息: {first_name} {last_name}")
            logger.info(f"邮箱: {email}")
            logger.info(f"学校: {school['name']}")
            logger.info(f"生日: {birth_date}")
            logger.info(f"验证ID: {self.verification_id}")

            # 生成文档
            pdf_data = generate_teacher_pdf(first_name, last_name)
            png_data = generate_teacher_png(first_name, last_name)

            pdf_size = len(pdf_data)
            png_size = len(png_data)

            # 动态执行 SheerID 步骤
            while True:
                step = self._get_current_step()
                logger.info(f"当前 SheerID 步骤: {step}")

                # Step 1: Personal Info
                if step == "collectPersonalInfo":
                    body = {
                        "firstName": first_name,
                        "lastName": last_name,
                        "birthDate": birth_date,
                        "email": email,
                        "phoneNumber": "",
                        "deviceFingerprintHash": self.device_fingerprint,
                        "locale": "en-US"
                    }
                    data, status = self._request(
                        "POST",
                        f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectPersonalInfo",
                        body
                    )
                    if status != 200:
                        raise Exception(data)
                    continue

                # Step 2: Teacher Info
               if step == "collectTeacherPersonalInfo":
    body = {
        # 🔥 REQUIRED AGAIN
        "firstName": first_name,
        "lastName": last_name,
        "email": email,

        # School info
        "organization": {
            "id": school["id"],
            "idExtended": school["idExtended"],
            "name": school["name"]
        },

        "employmentStatus": "ACTIVE",
        "deviceFingerprintHash": self.device_fingerprint,
        "locale": "en-US"
    }
                    data, status = self._request(
        "POST",
        f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/collectTeacherPersonalInfo",
        body
    )
    if status != 200:
        raise Exception(data)
    continue

                # Step 3: Skip SSO
                if step == "sso":
                    self._request(
                        "DELETE",
                        f"{SHEERID_BASE_URL}/rest/v2/verification/{self.verification_id}/step/sso"
                    )
                    continue

                # Step 4: Upload Docs
                if step == "docUpload":
                    break

                # 等待或成功
                if step in ("pending", "approved"):
                    return {
                        "success": True,
                        "pending": step == "pending",
                        "verification_id": self.verification_id
                    }

                # 错误状态
                if step == "error":
                    raise Exception("SheerID 已进入 error 状态，必须重新创建 verification")

            # 文档上传
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
                raise Exception("docUpload 失败")

            pdf_url = data["documents"][0]["uploadUrl"]
            png_url = data["documents"][1]["uploadUrl"]

            if not self._upload(pdf_url, pdf_data, "application/pdf"):
                raise Exception("PDF 上传失败")
            if not self._upload(png_url, png_data, "image/png"):
                raise Exception("PNG 上传失败")

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

        except Exception as e:
            logger.error(f"✗ 验证失败: {e}")
            return {
                "success": False,
                "verification_id": self.verification_id,
                "message": str(e)
            }
