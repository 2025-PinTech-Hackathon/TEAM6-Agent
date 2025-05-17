# agent/local_server/core/utils.py

import os
import platform


def get_chrome_path() -> str:
    system = platform.system()

    if system == "Windows":
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    elif system == "Darwin":
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    elif system == "Linux":
        chrome_path = "/usr/bin/google-chrome"
    else:
        raise FileNotFoundError(f"Unsupported operating system: {system}")

    if not os.path.exists(chrome_path):
        raise FileNotFoundError(f"Google Chrome executable not found at: {chrome_path}")

    return chrome_path
