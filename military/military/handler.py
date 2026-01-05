# military/handler.py

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from military.flow import MilitaryVerifier

(
    FIRST,
    LAST,
    EMAIL,
    DOB,
    BRANCH,
    STATUS
) = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["verification_id"] = context.args[0]
    await update.message.reply_text("First name:")
    return FIRST

async def first(update, context):
    context.user_data["first"] = update.message.text
    await update.message.reply_text("Last name:")
    return LAST

async def last(update, context):
    context.user_data["last"] = update.message.text
    await update.message.reply_text("Email:")
    return EMAIL

async def email(update, context):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("DOB (YYYY-MM-DD):")
    return DOB

async def dob(update, context):
    context.user_data["dob"] = update.message.text
    await update.message.reply_text("Branch (Army/Navy/Air Force/Marines):")
    return BRANCH

async def branch(update, context):
    context.user_data["branch"] = update.message.text
    await update.message.reply_text("Status (VETERAN or ACTIVE_DUTY):")
    return STATUS

async def finalize(update, context):
    context.user_data["status"] = update.message.text

    verifier = MilitaryVerifier(context.bot_data["SHEERID_TOKEN"])

    result = await verifier.verify(
        context.user_data["verification_id"],
        context.user_data["first"],
        context.user_data["last"],
        context.user_data["email"],
        context.user_data["dob"],
        context.user_data["branch"],
        context.user_data["status"]
    )

    await update.message.reply_text(
        f"Military Verification Result:\n{result.get('status')}"
    )
    return ConversationHandler.END
