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

# ===== User commands =====
from handlers.user_commands import (
    start_command,
    about_command,
    help_command,
    balance_command,
    checkin_command,
    invite_command,
    use_command,
)

# ===== Verify commands =====
from handlers.verify_commands import (
    verify_command,
    verify2_command,
    verify3_command,
    verify4_command,
    getV4Code_command,
)

# ===== Admin commands =====
from handlers.admin_commands import (
    addbalance_command,
    block_command,
    white_command,
    blacklist_command,
    genkey_command,
    listkeys_command,
    broadcast_command,
)

# ===== Military conversation handler =====
from military.handler import (
    start,
    first,
    last,
    email,
    dob,
    branch,
    finalize,
    FIRST,
    LAST,
    EMAIL,
    DOB,
    BRANCH,
    STATUS,
)

# ===== Logging =====
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


async def error_handler(update, context):
    logger.exception("处理更新时发生异常", exc_info=context.error)


def main():
    # ================= DATABASE =================
    db = Database()

    # ================= TELEGRAM APP =================
    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)
        .build()
    )

    # ================= SHEERID TOKEN PROVIDER =================
    if SHEERID_MODE == "REAL":
        token_provider = SheerIDTokenManager(
            client_id=SHEERID_CLIENT_ID,
            client_secret=SHEERID_CLIENT_SECRET,
            auth_url=SHEERID_OAUTH_URL,
        )
        application.bot_data["SHEERID_TOKEN_PROVIDER"] = token_provider
        logger.info("SheerID REAL mode enabled")
    else:
        application.bot_data["SHEERID_TOKEN_PROVIDER"] = None
        logger.info("SheerID MOCK mode enabled")

    # ================= USER COMMANDS =================
    application.add_handler(CommandHandler("start", partial(start_command, db=db)))
    application.add_handler(CommandHandler("about", partial(about_command, db=db)))
    application.add_handler(CommandHandler("help", partial(help_command, db=db)))
    application.add_handler(CommandHandler("balance", partial(balance_command, db=db)))
    application.add_handler(CommandHandler("qd", partial(checkin_command, db=db)))
    application.add_handler(CommandHandler("invite", partial(invite_command, db=db)))
    application.add_handler(CommandHandler("use", partial(use_command, db=db)))

    # ================= VERIFY COMMANDS =================
    application.add_handler(CommandHandler("verify", partial(verify_command, db=db)))
    application.add_handler(CommandHandler("verify2", partial(verify2_command, db=db)))
    application.add_handler(CommandHandler("verify3", partial(verify3_command, db=db)))
    application.add_handler(CommandHandler("verify4", partial(verify4_command, db=db)))
    application.add_handler(CommandHandler("getV4Code", partial(getV4Code_command, db=db)))

    # ================= MILITARY VERIFICATION =================
    military_handler = ConversationHandler(
        entry_points=[CommandHandler("verify_military", start)],
        states={
            FIRST: [MessageHandler(filters.TEXT & ~filters.COMMAND, first)],
            LAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, last)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email)],
            DOB: [MessageHandler(filters.TEXT & ~filters.COMMAND, dob)],
            BRANCH: [MessageHandler(filters.TEXT & ~filters.COMMAND, branch)],
            STATUS: [MessageHandler(filters.TEXT & ~filters.COMMAND, finalize)],
        },
        fallbacks=[],
        name="military_conversation",
        persistent=False,
    )
    application.add_handler(military_handler)

    # ================= ADMIN COMMANDS =================
    application.add_handler(CommandHandler("addbalance", partial(addbalance_command, db=db)))
    application.add_handler(CommandHandler("block", partial(block_command, db=db)))
    application.add_handler(CommandHandler("white", partial(white_command, db=db)))
    application.add_handler(CommandHandler("blacklist", partial(blacklist_command, db=db)))
    application.add_handler(CommandHandler("genkey", partial(genkey_command, db=db)))
    application.add_handler(CommandHandler("listkeys", partial(listkeys_command, db=db)))
    application.add_handler(CommandHandler("broadcast", partial(broadcast_command, db=db)))

    # ================= ERROR HANDLER =================
    application.add_error_handler(error_handler)

    # ================= START =================
    logger.info("机器人启动中...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
