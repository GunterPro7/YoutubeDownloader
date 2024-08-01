from typing import List

from src.main import gui_handler


def setname():
    name2 = str(gui_handler.name.get())
    if name2 == "":
        return
    else:
        if name2[-4:] == ".mp3" and str(gui_handler.mp3_mp4.get()) == "mp3" or name2[-4:] == ".mp4" and str(gui_handler.mp3_mp4.get()) == "mp4":
            return name2[:-4]

        else:
            return name2


def append_or_create_file(file_name: str, content: List[str]):
    pass
