import os
import sys
import time
from datetime import datetime
from enum import Enum

from src.gunterpro7.utils import file_utils

_default_color: str = '\033[38m'
_out_file: str = ""


def __init__():
    global _out_file
    _out_folder: str = os.getcwd() + "\\log\\"
    _out_file = _out_folder + "log" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".txt"
    os.makedirs(_out_folder, exist_ok=True)
    info("Initializing logger")


def success(*message: str) -> None:
    _print(' '.join(message), 32, _Type.success)


def log(*message: str) -> None:
    _print(' '.join(message), 38, _Type.log)


def info(*message: str) -> None:
    _print(' '.join(message), 34, _Type.info)


def warn(*message: str) -> None:
    _print(' '.join(message), 33, _Type.warn)


def error(*message: str) -> None:
    _print(' '.join(message), 31, _Type.error)


def fatal(*message: str) -> None:
    _print(' '.join(message), 31, _Type.fatal)
    time.sleep(2.5)
    sys.exit(0)


class _Type(Enum):
    success = 'success'
    log = 'log'
    info = 'info'
    warn = 'warn'
    error = 'error'
    fatal = 'fatal'


def _print(message: str, color: int, type: _Type) -> None:
    time_stamp: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print('\033[' + str(color) + 'm[' + time_stamp + "] " + message + _default_color)
    file_utils.append_or_create_file(_out_file, "[" + time_stamp + " " + type.name.upper() + "] " + message)




