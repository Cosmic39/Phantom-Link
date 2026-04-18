import os
import psutil
import pyautogui
import screen_brightness_control as sbc
import pyperclip
import time
import ctypes
import threading
from pathlib import Path

import utils.state as state


# ---------------- SYSTEM COMMANDS ---------------- #

def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")


def restart_pc():
    os.system("shutdown /r /t 1")


def shutdown_pc():
    os.system("shutdown /s /t 1")


# ---------------- SCREENSHOT ---------------- #

def screenshot(path="screenshot.png"):
    try:
        image = pyautogui.screenshot()
        image.save(path)
        return path
    except Exception as e:
        return f"Error taking screenshot: {e}"


# ---------------- AUDIO CONTROL ---------------- #

def mute_system():
    pyautogui.press("volumemute")


def unmute_system():
    pyautogui.press("volumemute")


def volume_up(steps=5):
    for _ in range(steps):
        pyautogui.press("volumeup")


def volume_down(steps=5):
    for _ in range(steps):
        pyautogui.press("volumedown")


# ---------------- BRIGHTNESS CONTROL ---------------- #

def set_brightness(value):
    try:
        sbc.set_brightness(value)
        return True
    except Exception as e:
        return f"Brightness error: {e}"


def brightness_up(step=10):
    try:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(min(100, current + step))
        return True
    except Exception as e:
        return f"Brightness error: {e}"


def brightness_down(step=10):
    try:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(max(0, current - step))
        return True
    except Exception as e:
        return f"Brightness error: {e}"


# ---------------- PROCESS CONTROL ---------------- #

def close_process(process_name):
    try:
        result = os.system(f"taskkill /f /im {process_name}")
        return result == 0
    except Exception:
        return False


# ---------------- RUNNING APPS ---------------- #

def list_running_apps(limit=20):
    processes = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            name = proc.info['name']
            pid = proc.info['pid']
            processes.append(f"{name} (PID: {pid})")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes = list(set(processes))
    processes.sort()

    return processes[:limit]


# ---------------- CLIPBOARD CONTROL ---------------- #

def get_clipboard():
    try:
        data = pyperclip.paste()
        return data if data else "Clipboard is empty."
    except Exception as e:
        return f"Error reading clipboard: {e}"


# ---------------- KEYBOARD TYPE FUNCTION ---------------- #

def type_text(text, interval=0.01, delay=1):
    time.sleep(delay)
    pyautogui.write(text, interval=interval)


# ---------------- 📢 MESSAGE BOX ---------------- #

def show_message_box(title, message, style=0):
    def run():
        ctypes.windll.user32.MessageBoxW(0, message, title, style)

    threading.Thread(target=run, daemon=True).start()


# ---------------- 📁 FILE SYSTEM ---------------- #

USER_HOME = str(Path.home())

COMMON_DIRS = {
    "desktop": os.path.join(USER_HOME, "Desktop"),
    "downloads": os.path.join(USER_HOME, "Downloads"),
    "documents": os.path.join(USER_HOME, "Documents"),
    "music": os.path.join(USER_HOME, "Music"),
    "pictures": os.path.join(USER_HOME, "Pictures"),
}


def get_file_path(base, filename):
    base = base.lower()

    # ✅ Safe folders
    if base in COMMON_DIRS:
        return os.path.join(COMMON_DIRS[base], filename), False

    # ⚠️ Custom path (restricted)
    if base.startswith("c:"):
        full_path = os.path.join(base, filename)

        blocked = ["windows", "system32", "program files"]
        if any(b in full_path.lower() for b in blocked):
            return None, None

        return full_path, True

    return None, None


# ---------------- 📤 FILE SAVE (UPLOAD SUPPORT) ---------------- #

def sanitize_filename(filename):
    return filename.replace("/", "").replace("\\", "").strip()


def save_uploaded_file(file_bytes, destination, filename):
    try:
        filename = sanitize_filename(filename)

        # Resolve path
        full_path, _ = get_file_path(destination, filename)

        if full_path is None:
            return None, "❌ Invalid destination."

        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        # Save file
        with open(full_path, "wb") as f:
            f.write(file_bytes)

        return full_path, "✅ File uploaded successfully"

    except Exception as e:
        return None, f"❌ Upload error: {e}"


# ---------------- 🟢 SYSTEM ACTIVITY ---------------- #

def get_system_active_status():
    try:
        now = time.time()
        diff = int(now - state.last_seen)

        if diff < 5:
            status = "🟢 Online"
            last = "Just now"
        elif diff < 60:
            status = "🟡 Idle"
            last = f"{diff} sec ago"
        else:
            status = "🔴 Possibly Offline"
            last = f"{diff} sec ago"

        return f"{status}\nLast Seen: {last}"

    except Exception as e:
        return f"Error getting status: {e}"