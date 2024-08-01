import os
import time
import tkinter as tk
from tkinter import ttk
from tkinter import *

from pytube import Playlist

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

# Values (set later)
counter_playlist = 0
playlist_last = ""
orig_name = "None"

def get_playlist_backwards_button():
    print(playlist_backwards_button)

# Global Variables
settings_ = True
mp3_mp4_var__ = "mp3"


def __main__():
    global root
    root = tk.Tk()


def __setup__():
    global c1, c2, c3

    label = tk.Label(root, fg="green")
    root.geometry("530x300")
    root.resizable(False, False)
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
                                command=prepare_download)
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
    link.trace('w', display_options)
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

    playlist_forward_button = tk.Button(root, text='', height=35, width=32, border=5, command=forwards_playlist,
                                        image=config.playlist_forwards)
    playlist_backwards_button = tk.Button(root, text='', height=35, width=32, border=5, command=backwards_playlist,
                                          image=config.playlist_backwards)

    advanced_using_button = tk.Button(root, text='', height=1, width=2, border=5, command=switch_advanced_using)
    playlist_same_quality = tk.Button(root, text='', height=1, width=2, border=5, command=switch_playlist_same_quality)


def download_yt_video(*args):
    root.title(language.get_idx(11))
    if args != ():
        result = downloader.download_yt_video_mp4(*args)
    else:
        result = downloader.download_yt_video_mp4(link.get(), mp3_mp4.get(), fast_fancy.get(),
                                                  option_lst.get()[:option_lst.get().find("p") + 1], option_lst.get())
    hidden_text.config(text=result)


def get_resolutions(link: str):
    download_button.place(x=400, y=212)
    return downloader.get_resolutions(link)


def display_options(*event):
    global lst_formats, resolutions, playlist_dropdown, counter_playlist, playlist_lst, playlist_formats, playlist_dropdown, playlist_last
    if link.get() == "":
        hidden_text.config(text=language.get_idx(20))
        text_title.config(text=language.get_idx(10))
        return
    if playlist_dropdown.get() == "Playlist":
        if playlist_last != link.get() or playlist_lst == []:
            text_title.config(text=language.get_idx(10))
            playlist_lst = Playlist(link.get()).video_urls
            try:
                playlist_formats = [
                    {"Format": "mp3", "Audio": language.get_idx(24), "Pixel": language.get_idx(21)} for _ in
                    range(len(playlist_lst))]
            except KeyError:
                hidden_text.config(text=language.get_idx(9))
                return
            counter_playlist = 0
            playlist_last = link.get()
            # formate zurücksetzen
            setIngameFormat()

    valid = downloader.valid_link(link.get())  # check the validity of link
    if not valid:
        hidden_text.config(text=language.get_idx(9))
        print("Loading Video/Audio Failed! Error: URL-Not Found 404")
        return

    hidden_text.config(text=language.get_idx(20))
    if playlist_dropdown.get() == "Playlist":
        url = playlist_lst[counter_playlist]
    else:
        url = link.get()
        options.set(language.get_idx(21))

    ydl_opts = {}
    resolutions = []
    lst_formats = []

    if "list" in url:
        url = url.split("&list")[0]
    print(url)

    video_data = get_resolutions(url)

    if playlist_dropdown.get() == "Video":
        text_title.config(text=f'{language.get_idx(10)} {video_data[1][:41]}')
    else:
        text_title.config(
            text=f'{language.get_idx(10)} {video_data[1][:33]} - {counter_playlist + 1} / {len(playlist_lst)}')

    options['values'] = video_data[0]  # sets combobox values to available resolutions


def prepare_download():
    global playlist_dropdown, playlist_lst
    while os.getcwd().split("\\")[-1] in ["Videos_Audios", "data", orig_name]:
        os.chdir("..")
    try:
        os.chdir("Videos_Audios")
    except FileNotFoundError:
        os.makedirs("Videos_Audios")
        os.chdir("Videos_Audios")
    time.sleep(0.15)
    if playlist_dropdown.get() == "Video":
        root.after(15, download_yt_video)
        hidden_text.config(text=language.get_idx(27) + " " * 45)
        download_button.place_forget()
        root.after(100, set_pixel_back)
    else:
        if name.get() == "":
            hidden_text.config(text=language.get_idx(14))
            return
        try:
            setPlaylistFormat()
        except NameError:
            hidden_text.config(text=language.get_idx(13))
            return
        download_button.place_forget()
        root.after(15, prepare_playlist_download)
        hidden_text.config(text=language.get_idx(27) + " 1/" + str(len(playlist_lst)) + " " * 30)


def prepare_playlist_download():
    global playlist_index, orig_name
    playlist_index = 0
    orig_name = name.get()
    print(orig_name)
    try:
        os.chdir(orig_name)
    except FileNotFoundError:
        os.makedirs(orig_name)
        os.chdir(orig_name)
    else:
        hidden_text.config(text=language.get_idx(15))
        return
    print("Downloading in directory --> " + os.getcwd())

    root.after(50, continue_downloading)


def continue_downloading():
    global playlist_lst, playlist_formats, playlist_index, orig_name
    try:
        prev_name = get_resolutions(playlist_lst[playlist_index])[1]
        download_button.place_forget()
        final_name = ""
        for a in prev_name:
            if a not in '\\/:*?<>|"':
                final_name += a

        name.set(final_name)
        if not config.switch_playlist_same_quality_var:
            download_yt_video(playlist_lst[playlist_index], playlist_formats[playlist_index]["Format"],
                                playlist_formats[playlist_index]["Audio"], playlist_formats[playlist_index]["Pixel"][
                                                                            :playlist_formats[playlist_index]["Pixel"].find(
                                                                                "p") + 1],
                                playlist_formats[playlist_index]["Pixel"])
        else:
            try:
                download_yt_video(playlist_lst[playlist_index], playlist_formats[0]["Format"],
                                    playlist_formats[0]["Audio"], playlist_formats[0]["Pixel"][
                                                                                :playlist_formats[0][
                                                                                    "Pixel"].find(
                                                                                    "p") + 1],
                                    playlist_formats[0]["Pixel"])
            except Exception as err:
                tempQuality = get_resolutions(playlist_lst[playlist_index])[0][-1]
                download_yt_video(playlist_lst[playlist_index], playlist_formats[0]["Format"],
                                    playlist_formats[0]["Audio"], tempQuality[
                                                                    :tempQuality.find(
                                                                        "p") + 1],
                                    tempQuality)
        hidden_text.config(
            text=language.get_idx(27) + " " + str(playlist_index + 2) + "/" + str(len(playlist_lst)) + " " * 30)
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            root.after(50, continue_downloading)
        else:
            hidden_text.config(
                text=language.get_idx(27) + " " + str(len(playlist_lst)) + "/" + str(len(playlist_lst)) + " " * 30)
            name.set(orig_name)
            set_pixel_back()
            hidden_text.config(text=language.get_idx(19))
            os.chdir("..")
            return
    except Exception:
        print("Video is age restricted! Skipping!")
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            root.after(50, continue_downloading)


def forwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        hidden_text.config(text=language.get_idx(28))
    if playlist_lst == []:
        hidden_text.config(text=language.get_idx(28))
        return
    if counter_playlist != len(playlist_lst) - 1:
        counter_playlist += 1
    else:
        hidden_text.config(text=language.get_idx(29))
        return
    setIngameFormat()


def backwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        hidden_text.config(text=language.get_idx(28))
    if playlist_lst == []:
        hidden_text.config(text=language.get_idx(28))
        return
    if counter_playlist != 0:
        counter_playlist -= 1
    else:
        hidden_text.config(text=language.get_idx(29))
        return
    setIngameFormat()


def change_playlist_vid(var):
    if var == "Playlist" and not config.switch_playlist_same_quality_var:
        playlist_forward_button.place(x=449, y=147)
        playlist_backwards_button.place(x=400, y=147)
    else:
        playlist_forward_button.place_forget()
        playlist_backwards_button.place_forget()
    display_options()


def setIngameFormat():
    global playlist_formats
    if playlist_formats[counter_playlist]["Format"] == "mp4":
        options.place(x=160, y=155)

        c2.place(x=0, y=0)
        c1.place_forget()
        mp3_mp4.set("mp4")
    else:
        options.place_forget()

        c1.place(x=0, y=0)
        c2.place_forget()
        mp3_mp4.set("mp3")
    global fast_fancy, option_lst
    fast_fancy.set(playlist_formats[counter_playlist]["Audio"])
    option_lst.set(playlist_formats[counter_playlist]["Pixel"])
    display_options()


def setPlaylistFormat():
    global counter_playlist, playlist_formats, mp3_mp4, option_lst

    new_format_dict = {"Format": mp3_mp4.get(), "Audio": fast_fancy.get(), "Pixel": option_lst.get()}
    playlist_formats[counter_playlist] = new_format_dict


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
