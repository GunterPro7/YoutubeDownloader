import os
from tkinter import *

from src.main import language
from src.main.language import language_dict
from src.utils import utils

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


def __main__():
    global set_bg, set_language
    set_bg = StringVar()
    set_language = StringVar()

    try:
        os.chdir("data")
    except FileNotFoundError:
        os.mkdir("data")
        os.chdir("data")

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
        with open("data.txt") as file:
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
        with open("data.txt") as file:
            user_data = str(file.read()).split(";")
            # read data
            print(*user_data)
            command_line = utils.to_bool(user_data[2])
            switch_advanced_using_var = utils.to_bool(user_data[2])
            switch_playlist_same_quality_var = utils.to_bool(user_data[3])

            language.set_language(str(user_data[0]))
            set_language.set(str(user_data[0]))

            set_bg.set(str(user_data[1]))
            bgImage = str(user_data[1])


def repair_data():
    print("Invalid data detected! Reseting data...")
    with open("data.txt", "w") as file:
        file.write("English;Bubbles;False;True")  # standards


def save_data():
    global switch_advanced_using_var
    os.chdir("..")
    try:
        os.chdir("data")
    except FileNotFoundError:
        os.makedirs("data")
        os.chdir("data")
    with open("data.txt", "w") as file:  # language, background, advanced using
        file.write(str(set_language.get()) + ";" + str(set_bg.get()) + ";" + str(switch_advanced_using_var) + ";" + str(switch_playlist_same_quality_var))
