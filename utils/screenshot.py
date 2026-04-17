import pyautogui

def take_screenshot(path="screenshot.png"):
    image = pyautogui.screenshot()
    image.save(path)
    return path