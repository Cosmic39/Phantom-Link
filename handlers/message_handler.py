import utils.state as state
from handlers.system_handler import shutdown_pc, restart_pc, save_uploaded_file
from utils.auth import SECRET_CODE

import time

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


async def handle_message(update, context):
    user_id = update.effective_user.id

    # ---------------- 🟢 UPDATE LAST SEEN ---------------- #
    state.last_seen = time.time()

    # ---------------- 🚨 CONFIRMATION HANDLER ---------------- #
    if update.message.text:
        text = update.message.text.strip()

        if user_id in state.waiting_for_code:
            action = state.waiting_for_code[user_id]

            if text == SECRET_CODE:
                if action == "shutdown":
                    shutdown_pc()
                    await update.message.reply_text("🛑 Shutting down PC...")

                elif action == "restart":
                    restart_pc()
                    await update.message.reply_text("🔄 Restarting PC...")

            else:
                await update.message.reply_text("❌ Wrong code. Action cancelled.")

            del state.waiting_for_code[user_id]
            return

    # ---------------- 📤 FILE UPLOAD HANDLER ---------------- #
    if user_id in state.upload_sessions:
        session = state.upload_sessions[user_id]

        # ⏱️ Timeout check
        if time.time() - session["start_time"] > state.UPLOAD_TIMEOUT:
            del state.upload_sessions[user_id]
            await update.message.reply_text("⚠️ Upload timed out. Try again.")
            return

        # ❌ No file sent
        if not update.message.document:
            await update.message.reply_text("⚠️ Please send a file.")
            return

        document = update.message.document

        # 📏 Size check
        if document.file_size > MAX_FILE_SIZE:
            await update.message.reply_text("❌ File too large (max 50MB).")
            del state.upload_sessions[user_id]
            return

        try:
            # 📥 Download file from Telegram
            file = await document.get_file()
            file_bytes = await file.download_as_bytearray()

            destination = session["destination"]
            filename = document.file_name

            # 💾 Save file
            path, msg = save_uploaded_file(file_bytes, destination, filename)

            await update.message.reply_text(msg)

        except Exception as e:
            await update.message.reply_text(f"❌ Upload failed: {e}")

        # 🔄 Clear session
        del state.upload_sessions[user_id]
        return

    # ---------------- ⚠️ IGNORE OTHER MESSAGES ---------------- #
    return