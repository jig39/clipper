import pygetwindow as gw
import pyautogui
import win32gui
import win32clipboard
import threading
import keyboard
import sys
from io import BytesIO
from PIL import Image
import pystray
from pystray import MenuItem,Menu

flg=False

def send_to_clipboard(image: Image.Image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

def copy_active_window_to_clipboard():
    active_window = gw.getActiveWindow()
    if active_window is None:
        return

    rect = win32gui.GetWindowRect(active_window._hWnd)
    x, y, right, bottom = rect
    width = right - x
    height = bottom - y

    screenshot = pyautogui.screenshot(region=(x, y, width, height))
    send_to_clipboard(screenshot)

def on_quit(icon, item):
    global flg
    flg=True
    icon.stop()

def create_icon():
    icon_image = Image.open("icon.png")
    menu=Menu(
        MenuItem('終了',on_quit)
    )
    icon = pystray.Icon("test_icon", icon_image,title='clipper App', menu=menu)
    icon.run()

def start_tray_icon():
    icon_thread = threading.Thread(target=create_icon)
    icon_thread.daemon = True
    icon_thread.start()

def main():
    #show icon
    start_tray_icon()
    
    while not flg:
        if keyboard.is_pressed("End"):
            copy_active_window_to_clipboard()
            while keyboard.is_pressed("End"):
                pass
            
    sys.exit()

if __name__ == "__main__":
    main()

#命名が未だに適当