import sys
import winreg
from pathlib import Path


APP_NAME = "AIAssistant"


def enable_startup():

    python_path = sys.executable

    project_path = Path(__file__).resolve().parent.parent
    main_file = project_path / "main.py"

    command = f'"{python_path}" "{main_file}"'

    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run",
        0,
        winreg.KEY_SET_VALUE
    )

    winreg.SetValueEx(
        key,
        APP_NAME,
        0,
        winreg.REG_SZ,
        command
    )

    winreg.CloseKey(key)


def disable_startup():

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)

    except FileNotFoundError:
        pass