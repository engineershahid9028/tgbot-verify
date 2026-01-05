"""Telegram 机器人主程序"""
import logging
from functools import partial

from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

# ===== Project config =====
from config import (
    BOT_TOKEN,
    SHEERID_MODE,
    SHEERID_CLIENT_ID,
    SHEERID_CLIENT_SECRET,
    SHEERID_OAUTH_URL,
)

from database_mysql import Database

# ===== SheerID OAuth token manager =====
from sheerid_auth import SheerIDTokenManager

# ===== Use
