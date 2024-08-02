import os
import sys
import time
from datetime import datetime
from enum import Enum

from src.gunterpro7.utils import file_utils

_default_color: str = '\033[37m'
_out_file: str = ""

_old_stdout: object
_old_stderr: object


def __init__():
    global _out_file, _old_stdout, _old_stderr
    _out_folder: str = os.getcwd() + "\\log\\"
    _out_file = _out_folder + "log" + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + ".txt"
    os.makedirs(_out_folder, exist_ok=True)

    _old_stdout = sys.stdout
    _old_stderr = sys.stderr

    sys.stdout = _CustomOutputStream()
    sys.stderr = _CustomErrorStream()

    info("Initializing logger")


def success(*message: str, end="\n") -> None:
    _print(' '.join(message), 32, _Type.success, end)


def log(*message: str, end="\n") -> None:
    _print(' '.join(message), 37, _Type.log, end)


def info(*message: str, end="\n") -> None:
    _print(' '.join(message), 34, _Type.info, end)


def warn(*message: str, end="\n") -> None:
    _print(' '.join(message), 33, _Type.warn, end)


def error(*message: str, end="\n") -> None:
    _print(' '.join(message), 31, _Type.error, end)


def fatal(*message: str, end="\n") -> None:
    _print(' '.join(message), 31, _Type.fatal, end)
    time.sleep(2.5)
    sys.exit(0)


class _CustomOutputStream:
    def write(self, message):
        log(str(message), end="")

    def flush(self):
        pass


class _CustomErrorStream:
    def write(self, message):
        error(str(message), end="")

    def flush(self):
        pass


class _Type(Enum):
    success = 'success'
    log = 'log'
    info = 'info'
    warn = 'warn'
    error = 'error'
    fatal = 'fatal'


def _print(message: str, color: int, type: _Type, end: str) -> None:
    time_stamp: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    prefix: str = "\r" if message.startswith("\r") else ""
    msg: str = prefix + '\033[' + str(color) + 'm[' + time_stamp + "] " + message.replace("\r", "") + _default_color + end
    if _old_stderr is not None and _old_stdout is not None:
        if type == _Type.error:
            _old_stderr.write(msg)
        else:
            _old_stdout.write(msg)
    file_utils.append_or_create_file(_out_file, "[" + time_stamp + " " + type.name.upper() + "] " +
                                     message.replace("\r", "").rstrip("\n"))




