import os
import tkinter as tk
from tkinter import ttk
from tkinter import *

from src.main import config, language, downloader

try:
    import win32con, win32gui
except ImportError or ModuleNotFoundError as e:
    win32installed = False

# Setup
root: tk.Tk

# Canvas
c1: tk.Canvas
c2: tk.Canvas
c3: tk.Canvas

# Canvas Content
download_button: tk.Button
advanced_using_button: tk.Button
playlist_same_quality: tk.Button
options: ttk.Combobox
link: StringVar
link_entry: tk.Entry
name: StringVar
name_entry: tk.Entry
mp3_mp4: StringVar
dropdown_mp_: OptionMenu
hidden_text: tk.Label
text_fps: tk.Label
fast_fancy: StringVar
audio_dropdown: OptionMenu
option_lst: StringVar
text_title: tk.Label
settings_button: tk.Button
settings_language: OptionMenu
bg_dropdown: OptionMenu
playlist_dropdown: StringVar
video_playlist_dropdown: OptionMenu
playlist_forward_button: tk.Button
playlist_backwards_button: tk.Button

def get_playlist_backwards_button():
    print(playlist_backwards_button)

# Global Variables
settings_ = True
mp3_mp4_var__ = "mp3"


def __main__():
    __setup__()

    try:
        os.chdir("data")
    except FileNotFoundError:
        os.mkdir("data")
        os.chdir("data")


def __before_main__():
    global root
    root = tk.Tk()


def __setup__():
    global c1, c2, c3

    label = tk.Label(root, fg="green")
    root.geometry("530x300")
    root.resizable(0, 0)
    root.title(language.get_idx(0))

    if config.command_line == "False" and win32installed:
        hide = win32gui.GetForegroundWindow()
        win32gui.ShowWindow(hide, win32con.SW_HIDE)

    init_canvas()
    init_canvas_content()

    if config.switch_advanced_using_var:
        advanced_using_button.config(text="✓")

    if config.switch_playlist_same_quality_var:
        playlist_same_quality.config(text="✓")


def __run__():
    root.mainloop()


def init_canvas():
    global c1, c2, c3, image_
    c1 = tk.Canvas(root, width=530, height=300)
    c1.place(x=0, y=0)

    c2 = tk.Canvas(root, width=530, height=300)

    set_bg_and_image(config.bgImage)

    c3 = tk.Canvas(root, width=530, height=300)
    c3.create_image(0, 0, image=config.icon_settingsBG)
    c3.create_text(52, 29, text=language.get_idx(6), font=('Comic Sans MS', 12, 'normal'), fill="white")
    c3.create_text(60, 63, text=language.get_idx(7), font=('Comic Sans MS', 12, 'normal'), fill="white")
    c3.create_text(80, 97, text=language.get_idx(8), font=('Comic Sans MS', 12, 'normal'), fill="white")
    c3.create_text(95, 131, text=language.get_idx(30), font=('Comic Sans MS', 12, 'normal'), fill="white")
    c3.create_text(130, 260, text=language.get_idx(23), font=('Comic Sans MS', 12, 'normal'), fill="white")

def init_canvas_content():
    global download_button, advanced_using_button, playlist_same_quality, options, link, link_entry, name, name_entry, mp3_mp4, dropdown_mp_, hidden_text, text_fps, fast_fancy, \
        audio_dropdown, option_lst, text_title, settings_button, settings_language, bg_dropdown, playlist_dropdown, \
        video_playlist_dropdown, playlist_forward_button, playlist_backwards_button

    link = StringVar()
    link_entry = tk.Entry(root, textvariable=link, font=('calibre', 10, 'normal'), width=49)
    link_entry.place(x=125, y=20)

    name = StringVar()
    name_entry = tk.Entry(root, textvariable=name, font=('calibre', 10, 'normal'), width=49)
    name_entry.place(x=125, y=55)

    mp3_mp4 = StringVar(root)
    mp3_mp4.set("mp3")

    dropdown_mp_ = OptionMenu(root, mp3_mp4, "mp3", "mp4", command=func_mp3_mp4)
    dropdown_mp_.place(x=125, y=100)

    download_button = tk.Button(root, text=language.get_idx(26), height=3, width=11, border=5,
                                command=downloader.prepare_download)
    download_button.place(x=400, y=212)

    hidden_text = tk.Label(root, text=language.get_idx(20), fg="black", font=('Comic Sans MS', 10, 'normal'),
                           highlightthickness=3)
    hidden_text.place(x=37, y=239)

    text_fps = tk.Label(root, text="Fps:", fg="black", font=('calibre', 10, 'normal'), highlightthickness=3)

    fast_fancy = StringVar()
    fast_fancy.set(language.get_idx(24))
    audio_dropdown = OptionMenu(root, fast_fancy, language.get_idx(24), language.get_idx(25))
    audio_dropdown.place(x=280, y=100)

    option_lst = StringVar()
    link.trace('w', downloader.display_options)
    option_lst.set(language.get_idx(21))
    options = ttk.Combobox(root, textvariable=option_lst, state="readonly", width=14)

    text_title = tk.Label(root, text=language.get_idx(10), fg="black", font=('Comic Sans MS', 8, 'normal'),
                          highlightthickness=3)
    text_title.place(x=37, y=217)

    settings_button = tk.Button(root, text='', height=35, width=32, border=5, command=func_settings,
                                image=config.icon_settings)
    settings_button.place(x=484, y=2)

    settings_language = OptionMenu(root, config.set_language, "English", "Deutsch")

    bg_dropdown = OptionMenu(root, config.set_bg, "Bubbles", "Hexagon", "Rose", "Plants", "Settings", command=set_bg_and_image)

    playlist_dropdown = StringVar()
    playlist_dropdown.set("Video")
    video_playlist_dropdown = OptionMenu(root, playlist_dropdown, "Video", "Playlist", command=change_playlist_vid)
    video_playlist_dropdown.place(x=430, y=100)

    playlist_forward_button = tk.Button(root, text='', height=35, width=32, border=5, command=downloader.forwards_playlist,
                                        image=config.playlist_forwards)
    playlist_backwards_button = tk.Button(root, text='', height=35, width=32, border=5, command=downloader.backwards_playlist,
                                          image=config.playlist_backwards)

    advanced_using_button = tk.Button(root, text='', height=1, width=2, border=5, command=switch_advanced_using)
    playlist_same_quality = tk.Button(root, text='', height=1, width=2, border=5, command=switch_playlist_same_quality)

def change_playlist_vid(var):
    downloader.change_playlist_vid(var)


def set_bg_and_image(image__):
    global image_
    image_ = PhotoImage(file=str(image__) + ".png")

    c1.create_image(0, 0, image=image_)

    c1.create_text(60, 29, text=language.get_idx(1), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(60, 63, text=language.get_idx(2), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(60, 115, text=language.get_idx(3), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(245, 115, text=language.get_idx(4), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(396, 115, text="Type:", font=('Comic Sans MS', 10, 'normal'), fill="white")

    c2.create_image(0, 0, image=image_)

    c2.create_text(60, 29, text=language.get_idx(1), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(60, 63, text=language.get_idx(2), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(60, 115, text=language.get_idx(3), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(83, 164, text=language.get_idx(5), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(245, 115, text=language.get_idx(4), font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(396, 115, text="Type:", font=('Comic Sans MS', 10, 'normal'), fill="white")


def func_settings():
    global settings_
    if settings_ == True:
        settings_ = False
        func_to_settings()
    else:
        settings_ = True
        func_back()


def func_to_settings():
    options.place_forget()

    c2.place_forget()
    c1.place_forget()
    dropdown_mp_.place_forget()
    settings_button.config(image=config.icon_back)
    link_entry.place_forget()
    name_entry.place_forget()
    text_title.place_forget()
    hidden_text.place_forget()
    download_button.place_forget()
    audio_dropdown.place_forget()
    video_playlist_dropdown.place_forget()
    playlist_forward_button.place_forget()
    playlist_backwards_button.place_forget()

    settings_language.place(x=100, y=15)
    bg_dropdown.place(x=118, y=50)
    advanced_using_button.place(x=150, y=85)
    playlist_same_quality.place(x=190, y=119)
    c3.place(x=0, y=0)


def func_back():
    global mp3_mp4_var__
    if mp3_mp4_var__ == "mp4":
        options.place(x=160, y=155)
        c2.place(x=0, y=0)
    else:
        c1.place(x=0, y=0)
    link_entry.place(x=125, y=20)
    name_entry.place(x=125, y=55)
    dropdown_mp_.place(x=125, y=100)
    settings_button.config(image=config.icon_settings)
    text_title.place(x=37, y=217)
    hidden_text.place(x=37, y=239)
    download_button.place(x=400, y=212)
    audio_dropdown.place(x=280, y=100)
    video_playlist_dropdown.place(x=430, y=100)
    if playlist_dropdown.get() == "Playlist" and not config.switch_playlist_same_quality_var:
        playlist_forward_button.place(x=449, y=147)
        playlist_backwards_button.place(x=400, y=147)

    settings_language.place_forget()
    bg_dropdown.place_forget()
    advanced_using_button.place_forget()
    playlist_same_quality.place_forget()
    c3.place_forget()

    config.save_data()


def switch_advanced_using():
    if not config.switch_advanced_using_var:
        advanced_using_button.config(text="✓")
    else:
        advanced_using_button.config(text="")

    config.switch_advanced_using_var = not config.switch_advanced_using_var


def switch_playlist_same_quality():
    if not config.switch_playlist_same_quality_var:
        playlist_same_quality.config(text="✓")
    else:
        playlist_same_quality.config(text="")

    config.switch_playlist_same_quality_var = not config.switch_playlist_same_quality_var


def func_mp3_mp4(var):
    global mp3_mp4_var__
    if var == "mp4":
        options.place(x=160, y=155)

        c2.place(x=0, y=0)
        c1.place_forget()
        mp3_mp4_var__ = "mp4"
    else:
        options.place_forget()

        c1.place(x=0, y=0)
        c2.place_forget()
        mp3_mp4_var__ = "mp3"


def set_pixel_back():
    options.set(language.get_idx(21))
    download_button.place(x=400, y=212)
