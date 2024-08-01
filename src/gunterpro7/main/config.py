import time, sys
from tkinter import *

from src.gunterpro7.logger.logger import *
from src.gunterpro7.main import language
from src.gunterpro7.main.language import language_dict
from src.gunterpro7.utils import utils

# Tkinter Buttons (Images)
icon_settings: PhotoImage
icon_back: PhotoImage
icon_settingsBG: PhotoImage
playlist_forwards: PhotoImage
playlist_backwards: PhotoImage


# Data
command_line: bool
switch_advanced_using_var: bool
switch_playlist_same_quality_var: bool
bgImage: str  # File path

# Canvas String Vars
set_bg: StringVar
set_language: StringVar

# Global Vars
data_file_path: str


def __main__():
    global set_bg, set_language, data_file_path
    set_bg = StringVar()
    set_language = StringVar()

    data_file_path = os.getenv('LOCALAPPDATA') + "\\GunterPro7\\youtubeToMp3\\"
    os.makedirs(data_file_path, exist_ok=True)

    print(os.getcwd())

    try:
        base_path = os.path.dirname(__file__)
        print(base_path)
        base_path_2 = os.path.abspath(os.path.join(base_path, os.pardir, os.pardir))
        print(os.path.join(base_path_2, 'resources', 'Rose.png'))
        photo = PhotoImage(file=os.path.join(base_path_2, 'resources', 'Rose.png'))
        print(str(photo))
    except Exception as e:
        print(str(e))

    time.sleep(10)
    try:
        os.chdir("src/resources")
    except FileNotFoundError:
        fatal("No Resources Folder... Exiting...")

    load_tkinter_buttons()
    load_data_file()


def load_tkinter_buttons():
    global icon_settings, icon_back, icon_settingsBG, playlist_forwards, playlist_backwards

    icon_settings = PhotoImage(file="settings_.png")
    icon_back = PhotoImage(file="back.png")
    icon_settingsBG = PhotoImage(file="SettingsBG.png")

    playlist_forwards = PhotoImage(file="forward.png")
    playlist_backwards = PhotoImage(file="backwards.png")


def load_data_file():
    global command_line, switch_advanced_using_var, switch_playlist_same_quality_var, bgImage

    try:
        with open(data_file_path + "data.txt") as file:
            user_data = str(file.read()).split(";")
            # check data
            if user_data[0] not in language_dict.keys():
                repair_data()
            _ = PhotoImage(file=str(user_data[1]) + ".png")
            if user_data[2] not in ["True", "False"]:
                repair_data()
            if user_data[3] not in ["True", "False"]:
                repair_data()
    except Exception:
        repair_data()
    finally:
        with open(data_file_path + "data.txt") as file:
            user_data = str(file.read()).split(";")
            # read data
            info("Loaded user data: " + '; '.join(user_data))
            command_line = utils.to_bool(user_data[2])
            switch_advanced_using_var = utils.to_bool(user_data[2])
            switch_playlist_same_quality_var = utils.to_bool(user_data[3])

            language.set_language(str(user_data[0]))
            set_language.set(str(user_data[0]))

            set_bg.set(str(user_data[1]))
            bgImage = str(user_data[1])


def repair_data():
    error("Invalid data detected! Reseting data...")
    with open(data_file_path + "data.txt", "w") as file:
        file.write("English;Bubbles;False;True")  # standards


def save_data():
    global switch_advanced_using_var
    with open(data_file_path + "data.txt", "w") as file:  # language, background, advanced using
        file.write(str(set_language.get()) + ";" + str(set_bg.get()) + ";" + str(switch_advanced_using_var) + ";" + str(switch_playlist_same_quality_var))
