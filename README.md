#PhantomLink — Remote PC Control via Telegram

**Developer: Cosmic**

PhantomLink is a lightweight automation and remote-control system that lets you control your PC using a Telegram bot.
You can lock your PC, take screenshots, control volume, manage apps, and even access your clipboard — all remotely.

---

# ⚡ Features

* 🔒 Lock / Restart / Shutdown PC
* 📸 Screenshot capture
* 🔊 Volume control (mute / up / down)
* 💡 Brightness control
* ❌ Kill processes
* 🧠 List running apps
* 📋 Clipboard access
* 🔐 Secure command execution (secret code)

---

# 🧠 Step 1 — Create a Telegram Bot

1. Open Telegram

2. Search for **@BotFather**

3. Send:

   ```
   /start
   ```

4. Then:

   ```
   /newbot
   ```

5. Follow instructions:

   * Set bot name
   * Set username

6. Copy your **BOT TOKEN**

---

# 🧠 Step 2 — Get Your User ID

1. Search for **@userinfobot**
2. Send:

   ```
   /start
   ```
3. Copy your **User ID**

---

# 📁 Step 3 — Project Structure

```
PhantomLink/
│
├── main.py
├── requirements.txt
├── handlers/
├── utils/
├── config/
│   └── secrets.json
├── icon/
│   └── Icon.ico
```

---

# 🔐 Step 4 — Configure `secrets.json`

Create file:

```
config/secrets.json
```

Add:

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "authorized_user_id": 123456789,
  "secret_code": "1234"
}
```

---

# ⚙️ Step 5 — Install Dependencies

Run:

```
pip install python-telegram-bot pyautogui psutil screen-brightness-control pyperclip
```

---

# ▶️ Step 6 — Run the Bot (Development)

```
python main.py
```

If everything is correct, you’ll see:

```
🚀 PhantomLink Bot Running...
```

---

# 📡 Step 7 — Use Commands

Send commands in Telegram:

```
/system lock
/system screenshot
/system mute
/system volup
/system brightness 50
/system apps
/system clipboard
/system kill chrome.exe
```

---

# 🔥 Step 8 — Convert to EXE

Install PyInstaller:

```
pip install pyinstaller
```

Build the executable:

```
pyinstaller --onefile --noconsole --name "PhantomLink" --icon=icon/Icon.ico main.py
```

---

# 📦 Step 9 — Final Folder Setup

After build, go to:

```
dist/
```

Copy `PhantomLink.exe` into your main folder:

```
PhantomLink/
│
├── PhantomLink.exe
├── config/
│   └── secrets.json
```

⚠️ **IMPORTANT:**

* Keep `config` folder in the same directory as `.exe`
* Do NOT rename `secrets.json`

---

# 🖥️ Step 10 — Add to Startup

### Open Startup Folder:

Press:

```
Win + R
```

Type:

```
shell:startup
```

---

### Add Shortcut:

1. Right-click `PhantomLink.exe` → Create Shortcut
2. Copy shortcut
3. Paste into Startup folder

---

### Optional (Recommended):

* Right-click shortcut → Properties
* Set **Run: Minimized**

---

# 🔐 Security Notes

* Only your Telegram ID can control the bot
* Sensitive commands like Shutdown and Restart require THE Authentication code
* Keep your `secrets.json` private

---

# ⚠️ Limitations

* Clipboard works only for text
* Some features may not work on lock screen
* Antivirus may flag the `.exe` (false positive, But You are Smart Enough to check the code Yourself)

---

# 🧠 Future Improvements

* GUI dashboard
* Live monitoring (CPU/RAM)
* Automation macros
* Encrypted config
* Remote file access

---

# 😈 Final Words

PhantomLink is more than a bot — it’s a **remote control system for your machine**.

This is a:

* A Telegram-controlled system
* A deployable Windows application
* A foundation for full automation

---

# 👤 Developer

**Cosmic**
Cyber Security Specialist · Developer · Automation Enthusiast

---

🔥 *Control your system. Automate everything. Stay in command.*
