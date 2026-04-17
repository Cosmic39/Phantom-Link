# 🚀 PhantomLink — Remote PC Automation via Telegram

**Developer: Cosmic**

PhantomLink is a lightweight remote automation system that allows you to control your Windows PC using a Telegram bot.

It supports system control, automation, clipboard access, and keyboard input injection — all through secure authenticated commands.

---

# ⚡ Features (Updated Version)

## 🖥️ System Control

* 🔒 Lock PC
* 🔄 Restart / Shutdown (with authentication)
* ❌ Kill processes
* 🧠 List running applications

## 🔊 Audio Control

* Mute / Unmute system
* Volume Up / Down

## 💡 Display Control

* Brightness Up / Down
* Set brightness (0–100)

## 📸 Utilities

* Screenshot capture
* Clipboard access (text + file export for large data)

## ⌨️ Automation Engine (NEW)

* Remote typing into active window:

```bash
/system type hello world
```

---

# 🧠 Step 1 — Create Telegram Bot

1. Open Telegram
2. Search BotFather
3. Run:

```bash
/newbot
```

4. Set bot name + username
5. Copy your Bot Token

---

# 🧠 Step 2 — Get Your Telegram User ID

Use a Telegram user info bot.

Send:

```bash
/start
```

Copy your numeric ID.

---

# 📁 Step 3 — Project Structure

```
PhantomLink/
│
├── main.py
├── requirements.txt
├── handlers/
│   └── system_handler.py
├── utils/
│   ├── auth.py
│   └── state.py
├── config/
│   └── secrets.json
├── icon/
│   └── Icon.ico
```

---

# 🔐 Step 4 — Configure secrets.json

Create:

```
config/secrets.json
```

```json
{
  "bot_token": "YOUR_BOT_TOKEN",
  "authorized_user_id": 123456789,
  "secret_code": "1234"
}
```

---

# ⚙️ Step 5 — Install Dependencies

```bash
pip install python-telegram-bot pyautogui psutil screen-brightness-control pyperclip
```

---

# ▶️ Step 6 — Run the Bot (Development)

```bash
python main.py
```

Expected output:

```
🚀 PhantomLink Bot Running...
```

---

# 📡 Step 7 — Available Commands

## 🖥️ System Commands

```
/system lock
/system restart
/system shutdown
/system screenshot
/system apps
/system kill chrome.exe
```

---

## 🔊 Audio Commands

```
/system mute
/system unmute
/system volup
/system voldown
```

---

## 💡 Brightness Commands

```
/system brightup
/system brightdown
/system brightness 50
```

---

## 📋 Clipboard

```
/system clipboard
```

---

## ⌨️ Typing Automation (NEW)

```
/system type hello world
```

Types text into the currently active window.

---

# 📦 Step 8 — Build EXE (Final Release)

Install PyInstaller:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --noconsole --name "PhantomLink" --icon=icon/Icon.ico main.py
```

---

# 📁 Step 9 — Final Release Structure

After build:

```
PhantomLink/
│
├── PhantomLink.exe
├── config/
│   └── secrets.json
```

⚠️ Important:

* config folder must stay next to .exe
* Do NOT rename secrets.json

---

# 🖥️ Step 10 — Add to Startup

Open startup folder:

```
Win + R → shell:startup
```

Add shortcut of:

```
PhantomLink.exe
```

Recommended:

* Set shortcut → Run Minimized

---

# 🔐 Security System

* Only authorized Telegram user can control the system
* Sensitive actions require authentication code
* Unauthorized users are blocked automatically

---

# ⚠️ Limitations

* Typing works only on active/focused window
* Clipboard is text-based only
* Some features may not work on lock screen
* Antivirus may flag EXE (false positive due to PyInstaller)

---

# 🧠 Future Upgrades

* Macro recorder (mouse + keyboard replay system)
* GUI dashboard
* Encrypted configuration system
* Background stealth mode
* Live system monitoring

---

# 👤 Developer

**Cosmic**
Cyber Security Specialist · Automation Developer · AI Enthusiast

---

🔥 Control your system. Automate everything. Stay in command.
