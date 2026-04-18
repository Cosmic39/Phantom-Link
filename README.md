# PhantomLink — Remote Administration Tool via Telegram

**Developer: Cosmic**

PhantomLink is a powerful remote automation system that lets you control your Windows PC using a Telegram bot with secure, session-based authentication.

It now includes file transfer, system monitoring, message injection, and automation features — all controlled remotely.

---

# ⚡ Features (Latest Version)

## 🔐 Security System

* User ID based access control
* Session-based authentication (20 min access)
* Confirmation system for critical actions (shutdown/restart)

---

## 🖥️ System Control

* 🔒 Lock PC
* 🔄 Restart / Shutdown (with confirmation code)
* ❌ Kill processes
* 🧠 List running applications

---

## 🔊 Audio Control

* Mute / Unmute
* Volume Up / Down

---

## 💡 Display Control

* Brightness Up / Down
* Set brightness (0–100)

---

## 📸 Utilities

* Screenshot capture
* Clipboard extraction (auto file export if large)

---

## ⌨️ Automation Engine

* Type text into active window

```bash
/system type Hello World
```

---

## 📢 Message Injection (NEW)

Display native Windows popup messages:

```bash
/system message Hello
/system message alert Warning!
/system message warning Be careful
/system message info System update
```

---

## 📁 File System (Download)

Download files from PC:

```bash
/system file desktop file.txt
/system file downloads report.pdf
/system file C:\\Users\\Name\\file.txt
```

⚠️ Restricted system paths are blocked automatically

---

## 📤 File Upload System (NEW)

Upload files to PC via Telegram:

```bash
/system upload desktop
```

Then send file → it will be saved automatically

✔ Max size: 50MB
✔ Timeout protected
✔ Safe directory handling

---

## 🟢 System Activity Tracking

```bash
/system active
```

Returns:

* Online / Idle / Offline status
* Last seen time

---

# 🧠 Step 1 — Create Telegram Bot

1. Open Telegram
2. Search BotFather
3. Run:

```bash
/newbot
```

4. Set name & username
5. Copy Bot Token

---

# 🧠 Step 2 — Get Your Telegram User ID

Use a Telegram ID bot and send:

```bash
/start
```

Copy your numeric ID

---

# 📁 Step 3 — Project Structure

```
PhantomLink/
│
├── main.py
├── requirements.txt
├── handlers/
│   ├── system_handler.py
│   └── message_handler.py
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
  "authorized_user_id": YOUR_USER_ID,
  "secret_code": "YOUR_AUTH_CODE"
}
```

---

# ⚙️ Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install python-telegram-bot pyautogui psutil screen-brightness-control pyperclip
```

---

# ▶️ Step 6 — Run the Bot

```bash
python main.py
```

Expected:

```
🚀 PhantomLink Bot Running...
```

---

# 📡 Step 7 — Full Command List

```
/system auth <code>
/system message <text>
/system message alert <text>
/system message warning <text>
/system message info <text>
/system file <location> <filename>
/system upload <location>
/system lock
/system restart
/system shutdown
/system screenshot
/system mute
/system unmute
/system volup
/system voldown
/system brightup
/system brightdown
/system brightness <0-100>
/system kill <process.exe>
/system apps
/system clipboard
/system type <text>
/system active
```

---

# 📦 Step 8 — Build EXE

Install:

```bash
pip install pyinstaller
```

Build:

```bash
pyinstaller --onefile --noconsole --name "PhantomLink" --icon=icon/Icon.ico main.py
```

---

# 📁 Step 9 — Final Release Structure

```
PhantomLink/
│
├── PhantomLink.exe
├── config/
│   └── secrets.json
```

⚠️ Important:

* Keep config folder next to .exe
* Do NOT rename secrets.json

---

# 🖥️ Step 10 — Add to Startup

Open:

```
Win + R → shell:startup
```

Add shortcut of:

```
PhantomLink.exe
```

Recommended:

* Run minimized

---

# 🔐 Security Notes

* Only authorized user can control system
* Session expires after 20 minutes
* Critical actions require code confirmation
* Dangerous system paths are blocked

---

# ⚠️ Limitations

* Typing works only on active window
* Clipboard supports text only
* File transfer limited to 50MB
* Some features may not work on lock screen
* EXE may trigger antivirus (PyInstaller false positive)

---

# 🧠 Future Upgrades

* File manager (list directories)
* Command history system
* System stats (CPU, RAM, battery)
* Macro automation engine
* GUI dashboard

---

# 👤 Developer

**Cosmic**
Cyber Security Specialist · Automation Developer · AI Enthusiast

---

🔥 Control your system. Automate everything. Stay in command.
