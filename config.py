"""全局配置文件"""
import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# ================= TELEGRAM =================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "engrshahid")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/Engineershahidmughal")

# ================= SHEERID =================
# MODE: MOCK or REAL  ✅ THIS WAS MISSING
SHEERID_MODE = os.getenv("SHEERID_MODE", "MOCK")

# Token (used in MOCK, ignored in REAL with OAuth)
SHEERID_TOKEN = os.getenv("SHEERID_TOKEN", "DUMMY_SHEERID_TOKEN")

# OAuth (REAL mode only)
SHEERID_CLIENT_ID = os.getenv("SHEERID_CLIENT_ID", "")
SHEERID_CLIENT_SECRET = os.getenv("SHEERID_CLIENT_SECRET", "")
SHEERID_OAUTH_URL = "https://services.sheerid.com/oauth/token"

# Program IDs (REAL mode only)
SHEERID_VETERANS_PROGRAM_ID = os.getenv(
    "SHEERID_VETERANS_PROGRAM_ID", ""
)

# ================= ADMIN =================
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID", "7575476523"))

# ================= POINT SYSTEM =================
VERIFY_COST = 1
CHECKIN_REWARD = 1
INVITE_REWARD = 2
REGISTER_REWARD = 1

# ================= HELP =================
HELP_NOTION_URL = "https://rhetorical-era-3f3.notion.site/dd78531dbac745af9bbac156b51da9cc"
