import json
import time
import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from utils.auth import is_authorized, SECRET_CODE
import utils.state as state

from handlers.message_handler import handle_message
from handlers.system_handler import (
    lock_pc,
    restart_pc,
    shutdown_pc,
    screenshot,
    mute_system,
    unmute_system,
    volume_up,
    volume_down,
    brightness_up,
    brightness_down,
    set_brightness,
    close_process,
    list_running_apps,
    get_clipboard,
    type_text,
    get_system_active_status,
    show_message_box,
    get_file_path
)

# Load config
with open("config/secrets.json") as f:
    config = json.load(f)

TOKEN = config["bot_token"]
AUTHORIZED_USER_ID = config["authorized_user_id"]

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB


# ---------------- 🔐 SESSION CHECK ---------------- #

def is_authenticated(user_id):
    if user_id not in state.auth_sessions:
        return False

    if time.time() > state.auth_sessions[user_id]:
        del state.auth_sessions[user_id]
        return False

    return True


# ---------------- SYSTEM COMMAND ---------------- #

async def system_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    state.last_seen = time.time()

    if not is_authorized(user_id):
        await update.message.reply_text("❌ Unauthorized access.")
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n"
            "/system auth <code>\n"
            "/system message <text>\n"
            "/system file <location> <filename>\n"
            "/system upload <location>\n"
            "/system lock\n"
            "/system restart\n"
            "/system shutdown\n"
            "/system screenshot\n"
            "/system mute/unmute\n"
            "/system volup/voldown\n"
            "/system brightup/brightdown\n"
            "/system brightness <0-100>\n"
            "/system kill <process.exe>\n"
            "/system apps\n"
            "/system clipboard\n"
            "/system type <text>\n"
            "/system active"
        )
        return

    cmd = context.args[0].lower()

    # ---------------- 🔐 AUTH ---------------- #
    if cmd == "auth":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system auth <code>")
            return

        if context.args[1] == SECRET_CODE:
            state.auth_sessions[user_id] = time.time() + state.AUTH_DURATION
            await update.message.reply_text("✅ Authorized for 20 minutes")
        else:
            await update.message.reply_text("❌ Invalid Code")
        return

    # ---------------- 🔐 SESSION CHECK ---------------- #
    if not is_authenticated(user_id):
        await update.message.reply_text("🔐 Unauthorized. Use /system auth <code>")
        return

    # ---------------- 📢 MESSAGE ---------------- #
    if cmd == "message":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system message <text>")
            return

        text = " ".join(context.args[1:])
        show_message_box("PhantomLink", text)
        await update.message.reply_text("📢 Message displayed.")
        return

    # ---------------- 📁 FILE DOWNLOAD ---------------- #
    elif cmd == "file":
        if len(context.args) < 3:
            await update.message.reply_text("⚠️ Usage: /system file <location> <filename>")
            return

        base = context.args[1]
        filename = context.args[2]

        full_path, needs_auth = get_file_path(base, filename)

        if full_path is None:
            await update.message.reply_text("❌ Invalid or blocked path.")
            return

        if needs_auth and not is_authenticated(user_id):
            await update.message.reply_text("🔐 Auth required for this path.")
            return

        if not os.path.exists(full_path):
            await update.message.reply_text("❌ File not found.")
            return

        if os.path.getsize(full_path) > MAX_FILE_SIZE:
            await update.message.reply_text("❌ File too large (max 50MB).")
            return

        try:
            with open(full_path, "rb") as f:
                await update.message.reply_document(f)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {e}")

        return

    # ---------------- 📤 FILE UPLOAD ---------------- #
    elif cmd == "upload":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system upload <location>")
            return

        destination = context.args[1]

        state.upload_sessions[user_id] = {
            "destination": destination,
            "start_time": time.time()
        }

        await update.message.reply_text("📤 Send the file (max 50MB).")
        return

    # ---------------- 🚨 CONFIRMATION ---------------- #
    elif cmd in ["shutdown", "restart"]:
        state.waiting_for_code[user_id] = cmd
        await update.message.reply_text(f"🔐 Enter confirmation code to confirm {cmd}:")
        return

    # ---------------- SYSTEM FEATURES ---------------- #

    elif cmd == "lock":
        lock_pc()
        await update.message.reply_text("🔒 PC Locked.")

    elif cmd == "screenshot":
        path = screenshot()
        if isinstance(path, str) and path.endswith(".png"):
            with open(path, "rb") as img:
                await update.message.reply_photo(photo=img)
        else:
            await update.message.reply_text(path)

    elif cmd == "mute":
        mute_system()
        await update.message.reply_text("🔇 Muted")

    elif cmd == "unmute":
        unmute_system()
        await update.message.reply_text("🔊 Unmuted")

    elif cmd == "volup":
        volume_up()
        await update.message.reply_text("🔊 Volume Increased")

    elif cmd == "voldown":
        volume_down()
        await update.message.reply_text("🔉 Volume Decreased")

    elif cmd == "brightup":
        res = brightness_up()
        await update.message.reply_text("💡 Brightness Increased" if res is True else res)

    elif cmd == "brightdown":
        res = brightness_down()
        await update.message.reply_text("🌙 Brightness Decreased" if res is True else res)

    elif cmd == "brightness":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system brightness <0-100>")
            return

        try:
            val = int(context.args[1])
            res = set_brightness(val)
            await update.message.reply_text(f"💡 Brightness set to {val}%" if res is True else res)
        except:
            await update.message.reply_text("❌ Invalid value")

    elif cmd == "kill":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system kill <process.exe>")
            return

        success = close_process(context.args[1])
        await update.message.reply_text("❌ Killed" if success else "⚠️ Failed")

    elif cmd == "apps":
        apps = list_running_apps()
        await update.message.reply_text("🧠 Running Apps:\n\n" + "\n".join(apps) if apps else "No apps")

    elif cmd == "clipboard":
        data = get_clipboard()

        if len(data) > 4000:
            with open("clipboard.txt", "w", encoding="utf-8") as f:
                f.write(data)
            await update.message.reply_document(open("clipboard.txt", "rb"))
        else:
            await update.message.reply_text(f"📋 {data}")

    elif cmd == "type":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system type <text>")
            return

        type_text(" ".join(context.args[1:]))
        await update.message.reply_text("⌨️ Typed.")

    elif cmd == "active":
        await update.message.reply_text(get_system_active_status())

    else:
        await update.message.reply_text("⚠️ Unknown system command.")


# ---------------- STARTUP ---------------- #

async def on_start(app):
    try:
        await app.bot.send_message(
            chat_id=AUTHORIZED_USER_ID,
            text="🟢 System Connected\n🔐 Awaiting Authorization..."
        )
    except Exception as e:
        print(f"Startup message failed: {e}")


# ---------------- MAIN ---------------- #

def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.post_init = on_start

    app.add_handler(CommandHandler("system", system_command))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("🚀 PhantomLink Bot Running...")
    app.run_polling()


# ---------------- RETRY LOOP ---------------- #

if __name__ == "__main__":
    while True:
        try:
            print("🌐 Connecting...")
            run_bot()
        except Exception as e:
            print(f"⚠️ Connection lost: {e}")
            print("🔁 Retrying in 10s...")
            time.sleep(10)
