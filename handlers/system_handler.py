import os
import psutil
import pyautogui
import screen_brightness_control as sbc
import pyperclip


# ---------------- SYSTEM COMMANDS ---------------- #

def lock_pc():
    os.system("rundll32.exe user32.dll,LockWorkStation")


def restart_pc():
    os.system("shutdown /r /t 1")


def shutdown_pc():
    os.system("shutdown /s /t 1")


# ---------------- SCREENSHOT ---------------- #

def screenshot(path="screenshot.png"):
    image = pyautogui.screenshot()
    image.save(path)
    return path


# ---------------- AUDIO CONTROL (STABLE METHOD) ---------------- #

def mute_system():
    pyautogui.press("volumemute")


def unmute_system():
    pyautogui.press("volumemute")  # toggle


def volume_up(steps=5):
    for _ in range(steps):
        pyautogui.press("volumeup")


def volume_down(steps=5):
    for _ in range(steps):
        pyautogui.press("volumedown")


# ---------------- BRIGHTNESS CONTROL ---------------- #

def set_brightness(value):
    sbc.set_brightness(value)


def brightness_up(step=10):
    current = sbc.get_brightness()[0]
    sbc.set_brightness(min(100, current + step))


def brightness_down(step=10):
    current = sbc.get_brightness()[0]
    sbc.set_brightness(max(0, current - step))


# ---------------- PROCESS CONTROL ---------------- #

def close_process(process_name):
    os.system(f"taskkill /f /im {process_name}")


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