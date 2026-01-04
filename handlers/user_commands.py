"""User command handlers (English)"""

import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database
from utils.checks import reject_group_command
from utils.messages import (
    get_welcome_message,
    get_about_message,
    get_help_message,
)

logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or ""
    full_name = user.full_name or ""

    if db.user_exists(user_id):
        await update.message.reply_text(
            f"👋 Welcome back, {full_name}!\n\n"
            "You are already registered.\n"
            "Send /help to see available commands."
        )
        return

    invited_by: Optional[int] = None
    if context.args:
        try:
            invited_by = int(context.args[0])
            if not db.user_exists(invited_by):
                invited_by = None
        except Exception:
            invited_by = None

    if db.create_user(user_id, username, full_name, invited_by):
        await update.message.reply_text(
            get_welcome_message(full_name, bool(invited_by))
        )
    else:
        await update.message.reply_text(
            "❌ Registration failed. Please try again later."
        )


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return
    await update.message.reply_text(get_about_message())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return

    is_admin = update.effective_user.id == ADMIN_USER_ID
    await update.message.reply_text(get_help_message(is_admin))


async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text(
            "🚫 You are blocked from using this bot."
        )
        return

    user = db.get_user(user_id)
    if not user:
        await update.message.reply_text(
            "❗ You are not registered yet. Use /start first."
        )
        return

    await update.message.reply_text(
        f"💰 Your balance\n\n"
        f"Credits: {user['balance']}"
    )


async def invite_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("🚫 You are blocked.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Use /start to register first.")
        return

    bot_username = context.bot.username
    invite_link = f"https://t.me/{bot_username}?start={user_id}"

    await update.message.reply_text(
        f"🎁 Your invite link:\n{invite_link}\n\n"
        "You earn **2 credits** for every successful invite."
    )


async def use_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if await reject_group_command(update):
        return

    user_id = update.effective_user.id

    if db.is_user_blocked(user_id):
        await update.message.reply_text("🚫 You are blocked.")
        return

    if not db.user_exists(user_id):
        await update.message.reply_text("Use /start to register first.")
        return

    if not context.args:
        await update.message.reply_text(
            "Usage:\n/use <key>\n\nExample:\n/use ABCD1234"
        )
        return

    key_code = context.args[0].strip()
    result = db.use_card_key(key_code, user_id)

    if result is None:
        await update.message.reply_text("❌ Invalid key.")
    elif result == -1:
        await update.message.reply_text("❌ This key has reached its usage limit.")
    elif result == -2:
        await update.message.reply_text("❌ This key has expired.")
    elif result == -3:
        await update.message.reply_text("❌ You have already used this key.")
    else:
        user = db.get_user(user_id)
        await update.message.reply_text(
            f"✅ Key redeemed successfully!\n\n"
            f"Credits added: {result}\n"
            f"Current balance: {user['balance']}"
        )
