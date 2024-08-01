import ctypes
import subprocess
import threading
from typing import Dict, List

from src.gunterpro7.logger.logger import *
from src.gunterpro7.main import language

modules_to_check = {
    "pytube": True,
    "pytubefix": False,
    "youtube-dl": True,
    "tk": True,
    "pillow": True,
    "moviepy": True,
    # "ffmpeg": True,  # TODO test on VB, unsure if need and if how to install
    "pywin32": False,
}


def __main__():
    global modules_to_check

    modules_checked: Dict[str, bool] = {}
    installs_required: List[str] = []

    threads = []

    for key, value in modules_to_check.items():
        thread = threading.Thread(target=lambda: check_module(key, value, modules_checked, installs_required))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Ausgabe der Ergebnisse
    for module, is_installed in modules_checked.items():
        log(f"Module '{module}' is installed: {is_installed}")

    try:
        with open("data/data.txt") as file:
            user_data = str(file.read()).split(";")
            language_str = user_data[0]
    except Exception as e:
        error("Error while reading data file for language in initialization! Error: " + str(e))

    if len(installs_required) > 0 and ask_for_install(language_str, installs_required):
        for module in installs_required:
            log(f"Module '{module}' is required, installing...")
            install_module(module)


def ask_for_install(language_str: str, modules_to_install: list) -> bool:
    string: str = language.get_idx_in_lang(language_str, 31) + "\n"
    for module in modules_to_install:
        string += "- " + module + "\n"

    response = ctypes.windll.user32.MessageBoxW(0, string, language.get_idx_in_lang(language_str, 32), 3)
    if response == 6:
        return True
    elif response == 7 or response == 2:
        ctypes.windll.user32.MessageBoxW(0, language.get_idx_in_lang(language_str, 33),
                                         language.get_idx_in_lang(language_str, 32), 0)
        fatal("Cancelled Installation by user, program closing!")
    else:
        return False


def check_module(module: str, necessary: bool, result_dict: dict, installs_required: list):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'show', module], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        result_dict[module] = True
    except subprocess.CalledProcessError:
        result_dict[module] = False
        if necessary:
            installs_required.append(module)


def install_module(module: str):
    """
        Install a Python module using pip.

        :param module: Name of the module to install
        """
    try:
        # Use subprocess to call pip install
        result = subprocess.run([sys.executable, "-m", "pip", "install", module],
                                check=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        for line in result.stdout.splitlines():
            log(line)
        for line in result.stderr.splitlines():
            warn(line)

    except subprocess.CalledProcessError as e:
        # Handle the error if the pip install command fails
        print(f"Error occurred while installing module '{module}':")
        print(e.stderr)
        # Optionally re-raise the error or handle it as needed
        raise
