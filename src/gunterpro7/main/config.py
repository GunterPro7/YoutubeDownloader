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
resources_main_path: str


def __main__():
    global set_bg, set_language, data_file_path, resources_main_path
    set_bg = StringVar()
    set_language = StringVar()

    data_file_path = os.path.join(os.getcwd(), "_internal")
    os.makedirs(data_file_path, exist_ok=True)
    resources_main_path = os.getcwd()

    load_tkinter_buttons()
    load_data_file()


def load_tkinter_buttons():
    global icon_settings, icon_back, icon_settingsBG, playlist_forwards, playlist_backwards

    main_path: str = get_resources_path()

    icon_settings = PhotoImage(file=os.path.join(main_path, "settings_.png"))
    icon_back = PhotoImage(file=os.path.join(main_path, "back.png"))
    icon_settingsBG = PhotoImage(file=os.path.join(main_path, "SettingsBG.png"))

    playlist_forwards = PhotoImage(file=os.path.join(main_path, "forward.png"))
    playlist_backwards = PhotoImage(file=os.path.join(main_path, "backwards.png"))


def get_resources_path():
    return os.path.join(resources_main_path, '_internal', 'resources')


def load_data_file():
    global command_line, switch_advanced_using_var, switch_playlist_same_quality_var, bgImage

    try:
        with open(os.path.join(data_file_path, "data.txt")) as file:
            user_data = str(file.read()).split(";")
            # check data
            if user_data[0] not in language_dict.keys():
                repair_data()
            if user_data[2] not in ["True", "False"]:
                repair_data()
            if user_data[3] not in ["True", "False"]:
                repair_data()
    except Exception:
        repair_data()
    finally:
        with open(os.path.join(data_file_path, "data.txt")) as file:
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
    with open(os.path.join(data_file_path, "data.txt"), "w") as file:
        file.write("English;Bubbles;False;True")  # standards


def save_data():
    global switch_advanced_using_var
    with open(os.path.join(data_file_path, "data.txt"), "w") as file:  # language, background, advanced using
        file.write(str(set_language.get()) + ";" + str(set_bg.get()) + ";" + str(switch_advanced_using_var) + ";" + str(switch_playlist_same_quality_var))
