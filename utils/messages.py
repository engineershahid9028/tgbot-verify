"""Message templates (English)"""

from config import CHANNEL_URL, VERIFY_COST


def get_welcome_message(full_name: str, invited_by: bool = False) -> str:
    """Welcome message"""
    msg = (
        f"🎉 Welcome, {full_name}!\n"
        "You have successfully registered and received **1 credit**.\n"
    )

    if invited_by:
        msg += "Thanks for joining via an invite link. The inviter received **2 credits**.\n"

    msg += (
        "\n🤖 This bot automatically completes SheerID verification.\n\n"
        "Quick start:\n"
        "/about - Learn what this bot does\n"
        "/balance - Check your balance\n"
        "/help - View all commands\n\n"
        "Earn more credits:\n"
        "/qd - Daily check-in\n"
        "/invite - Invite friends\n\n"
        f"📢 Join our channel: {CHANNEL_URL}"
    )
    return msg


def get_about_message() -> str:
    """About message"""
    return (
        "🤖 SheerID Automatic Verification Bot\n\n"
        "Features:\n"
        "- Automatic SheerID student / teacher verification\n"
        "- Supports:\n"
        "  • Gemini One Pro\n"
        "  • ChatGPT Teacher K12\n"
        "  • Spotify Student\n"
        "  • YouTube Student Premium\n"
        "  • Bolt.new Teacher\n\n"
        "How to earn credits:\n"
        "- Register: +1 credit\n"
        "- Daily check-in: +1 credit\n"
        "- Invite friends: +2 credits per user\n"
        "- Redeem keys (based on key rules)\n"
        f"- Join channel: {CHANNEL_URL}\n\n"
        "How to use:\n"
        "1. Start verification on the official website\n"
        "2. Copy the **full verification URL** from your browser\n"
        "3. Send /verify, /verify2, /verify3, /verify4 or /verify5 with the link\n"
        "4. Wait for the result\n"
        "5. Bolt.new verification can auto-fetch the reward code\n"
        "   (or use /getV4Code <verification_id>)\n\n"
        "Send /help to see all commands"
    )


def get_help_message(is_admin: bool = False) -> str:
    """Help message"""
    msg = (
        "📖 SheerID Verification Bot — Help\n\n"
        "User commands:\n"
        "/start - Register / start using the bot\n"
        "/about - About this bot\n"
        "/balance - Check your balance\n"
        "/qd - Daily check-in (+1 credit)\n"
        "/invite - Generate invite link (+2 credits per user)\n"
        "/use <key> - Redeem a key\n\n"
        f"/verify <link> - Gemini One Pro (−{VERIFY_COST} credits)\n"
        f"/verify2 <link> - ChatGPT Teacher K12 (−{VERIFY_COST} credits)\n"
        f"/verify3 <link> - Spotify Student (−{VERIFY_COST} credits)\n"
        f"/verify4 <link> - Bolt.new Teacher (−{VERIFY_COST} credits)\n"
        f"/verify5 <link> - YouTube Student Premium (−{VERIFY_COST} credits)\n\n"
        "/getV4Code <verification_id> - Get Bolt.new reward code\n"
        
    )

    if is_admin:
        msg += (
            "\n🔐 Admin commands:\n"
            "/addbalance <user_id> <amount> - Add credits\n"
            "/block <user_id> - Block a user\n"
            "/white <user_id> - Unblock a user\n"
            "/blacklist - View blocked users\n"
            "/genkey <key> <credits> [uses] [days] - Generate redeem key\n"
            "/listkeys - List all keys\n"
            "/broadcast <message> - Send message to all users\n"
        )

    return msg


def get_insufficient_balance_message(current_balance: int) -> str:
    """Insufficient balance message"""
    return (
        f"❌ Insufficient balance!\n"
        f"Required: {VERIFY_COST} credits\n"
        f"Current: {current_balance} credits\n\n"
        "How to earn credits:\n"
        "- Daily check-in: /qd\n"
        "- Invite friends: /invite\n"
        "- Redeem a key: /use <key>"
    )


def get_verify_usage_message(command: str, service_name: str) -> str:
    """Verify command usage message"""
    return (
        f"Usage: {command} <SheerID link>\n\n"
        "Example:\n"
        f"{command} https://services.sheerid.com/verify/xxx/?verificationId=xxx\n\n"
        "How to get the link:\n"
        f"1. Open the {service_name} verification page\n"
        "2. Start the verification process\n"
        "3. Copy the **full URL** from the browser address bar\n"
        f"4. Send it using the {command} command"
    )











