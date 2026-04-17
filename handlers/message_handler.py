from utils.auth import SECRET_CODE
from utils.state import waiting_for_code
from handlers.system_handler import shutdown_pc, restart_pc

async def handle_message(update, context):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    # Check if user is waiting for verification
    if user_id in waiting_for_code:
        action = waiting_for_code[user_id]

        if text == SECRET_CODE:
            if action == "shutdown":
                shutdown_pc()
                await update.message.reply_text("✅ Shutting down PC...")

            elif action == "restart":
                restart_pc()
                await update.message.reply_text("🔄 Restarting PC...")

        else:
            await update.message.reply_text("❌ Wrong code. Action cancelled.")

        # Clear state after attempt
        del waiting_for_code[user_id]

    else:
        # No pending action
        await update.message.reply_text(
            "⚠️ No pending action.\nUse /system command first."
        )