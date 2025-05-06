import pygetwindow as gw
import win32gui
import win32clipboard
import threading
import keyboard
import sys
from io import BytesIO
from PIL import Image
import mss
import pystray
from pystray import MenuItem, Menu

#終了フラグ
exit_event = threading.Event()

def send_to_clipboard(image: Image.Image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

# アクティブウィンドウのスクショコピー
def copy_active_window_to_clipboard():
    active_window = gw.getActiveWindow()
    if active_window is None:
        return

    rect = win32gui.GetWindowRect(active_window._hWnd)
    x, y, right, bottom = rect
    width = right - x
    height = bottom - y

    with mss.mss() as sct:
        monitor = {"top": y, "left": x, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)
        send_to_clipboard(img)

def on_quit(icon, item):
    icon.stop()
    print('アプリ終了')
    exit_event.set()

def create_icon():
    icon_image = Image.open("icon.png")
    menu = Menu(MenuItem('終了', on_quit))
    icon = pystray.Icon("clipper", icon_image, "Clipper App", menu)
    icon.run()

def start_tray_icon():
    icon_thread = threading.Thread(target=create_icon)
    icon_thread.daemon = True
    icon_thread.start()

def main():
    start_tray_icon()
    print("Clipper 起動中：Endキーでアクティブウィンドウをコピー、トレイから終了可")
    while not exit_event.is_set():
        if keyboard.is_pressed("End"):
            copy_active_window_to_clipboard()
            while keyboard.is_pressed("End"):
                pass

if __name__ == "__main__":
    main()