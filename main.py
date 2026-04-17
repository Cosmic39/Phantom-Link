import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from utils.auth import is_authorized
from utils.state import waiting_for_code

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
    get_clipboard   # ✅ NEW IMPORT
)

# Load config
with open("config/secrets.json") as f:
    config = json.load(f)

TOKEN = config["bot_token"]

# ---------------- SYSTEM COMMAND ---------------- #

async def system_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_authorized(user_id):
        await update.message.reply_text("❌ Unauthorized access.")
        return

    if len(context.args) == 0:
        await update.message.reply_text(
            "Usage:\n"
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
            "/system clipboard"   # ✅ NEW
        )
        return

    cmd = context.args[0].lower()

    # 🔐 Requires confirmation
    if cmd in ["shutdown", "restart"]:
        waiting_for_code[user_id] = cmd
        await update.message.reply_text(f"🔐 Enter Authentication code to confirm {cmd}:")
        return

    # 🔒 Lock
    elif cmd == "lock":
        lock_pc()
        await update.message.reply_text("🔒 PC Locked.")

    # 📸 Screenshot
    elif cmd == "screenshot":
        path = screenshot()
        with open(path, "rb") as img:
            await update.message.reply_photo(photo=img)

    # 🔊 Volume Controls
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

    # 💡 Brightness Controls
    elif cmd == "brightup":
        brightness_up()
        await update.message.reply_text("💡 Brightness Increased")

    elif cmd == "brightdown":
        brightness_down()
        await update.message.reply_text("🌙 Brightness Decreased")

    elif cmd == "brightness":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system brightness <0-100>")
            return

        try:
            value = int(context.args[1])
            set_brightness(value)
            await update.message.reply_text(f"💡 Brightness set to {value}%")
        except:
            await update.message.reply_text("❌ Invalid brightness value")

    # ❌ Kill Process
    elif cmd == "kill":
        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Usage: /system kill <process.exe>")
            return

        process = context.args[1]
        close_process(process)
        await update.message.reply_text(f"❌ Killed {process}")

    # 🧠 List Running Apps
    elif cmd == "apps":
        apps = list_running_apps()

        if not apps:
            await update.message.reply_text("No running apps found.")
            return

        message = "🧠 Running Apps:\n\n" + "\n".join(apps)
        await update.message.reply_text(message)

    # 📋 CLIPBOARD (NEW FEATURE)
    elif cmd == "clipboard":
        data = get_clipboard()

        if len(data) > 4000:
            with open("clipboard.txt", "w", encoding="utf-8") as f:
                f.write(data)

            await update.message.reply_document(open("clipboard.txt", "rb"))
        else:
            await update.message.reply_text(f"📋 Clipboard:\n\n{data}")

    else:
        await update.message.reply_text("⚠️ Unknown system command.")

# ---------------- MAIN ---------------- #

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Command
    app.add_handler(CommandHandler("system", system_command))

    # Message (for secret code)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("PhantomLink Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()