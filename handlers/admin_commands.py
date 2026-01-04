"""Admin command handlers (English)"""

from telegram import Update
from telegram.ext import ContextTypes

from config import ADMIN_USER_ID
from database_mysql import Database


def _is_admin(update: Update) -> bool:
    return update.effective_user.id == ADMIN_USER_ID


async def addbalance_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Usage:\n/addbalance <user_id> <amount>"
        )
        return

    user_id = int(context.args[0])
    amount = int(context.args[1])

    db.add_balance(user_id, amount)
    await update.message.reply_text(
        f"✅ Added {amount} credits to user {user_id}."
    )


async def block_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    user_id = int(context.args[0])
    db.block_user(user_id)
    await update.message.reply_text(f"🚫 User {user_id} blocked.")


async def white_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    user_id = int(context.args[0])
    db.unblock_user(user_id)
    await update.message.reply_text(f"✅ User {user_id} unblocked.")


async def blacklist_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    users = db.get_blacklist()
    if not users:
        await update.message.reply_text("Blacklist is empty.")
        return

    msg = "🚫 Blocked users:\n"
    for u in users:
        msg += f"- {u}\n"

    await update.message.reply_text(msg)


async def genkey_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    await update.message.reply_text("✅ Key generated.")


async def listkeys_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    keys = db.list_keys()
    if not keys:
        await update.message.reply_text("No keys available.")
        return

    msg = "🔑 Keys:\n"
    for k in keys:
        msg += f"{k}\n"

    await update.message.reply_text(msg)


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE, db: Database):
    if not _is_admin(update):
        await update.message.reply_text("❌ Admin only.")
        return

    message = " ".join(context.args)
    users = db.get_all_users()

    for uid in users:
        try:
            await context.bot.send_message(uid, message)
        except Exception:
            pass

    await update.message.reply_text("📢 Broadcast sent.")
