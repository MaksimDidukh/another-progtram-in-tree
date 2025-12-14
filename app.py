import pystray
from PIL import Image, ImageDraw
import keyboard
import pygetwindow as gw
import win32gui
import win32con
import threading

# Словарь для хранения скрытых окон: {id_иконки: дескриптор_окна}
hidden_windows = {}

def create_image():
    """Создает простую иконку для трея (синий квадрат)."""
    width, height = 64, 64
    image = Image.new('RGB', (width, height), (0, 120, 215))
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 4, height // 4, width * 3 // 4, height * 3 // 4), fill=(255, 255, 255))
    return image

def show_window(icon, item):
    """Возвращает окно на экран и убирает иконку из трея."""
    hwnd = hidden_windows.get(icon)
    if hwnd:
        # Показываем окно
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        # Разворачиваем, если оно было минимизировано
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        # Выводим на передний план
        win32gui.SetForegroundWindow(hwnd)
        icon.stop()
        del hidden_windows[icon]

def hide_current_window():
    """Скрывает активное окно и создает иконку в трее."""
    hwnd = win32gui.GetForegroundWindow()
    if not hwnd:
        return

    window_title = win32gui.GetWindowText(hwnd)
    if not window_title:
        window_title = "Окно без названия"

    # Скрываем окно
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # Создаем иконку для этого окна
    icon = pystray.Icon(window_title, create_image(), title=f"Восстановить: {window_title}")
    icon.menu = pystray.Menu(pystray.MenuItem("Развернуть", show_window))
    
    hidden_windows[icon] = hwnd
    
    # Запускаем иконку в отдельном потоке
    threading.Thread(target=icon.run, daemon=True).start()
    print(f"Скрыто окно: {window_title}")

print("Скрипт запущен!")
print("Нажмите Ctrl + Shift + H, чтобы свернуть активное окно в трей.")

# Регистрируем горячую клавишу
keyboard.add_hotkey('ctrl+shift+h', hide_current_window)

# Держим программу запущенной
keyboard.wait()
