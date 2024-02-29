import time

win32installed = True

try:
    import os
    from pytube import YouTube, Playlist
    import tkinter as tk
    from tkinter import ttk
    import youtube_dl
    from tkinter import *
    from PIL import ImageTk
    import win32gui, win32con
    import moviepy.editor as mpe
except ModuleNotFoundError:
    win32installed = False
except ImportError as e:
    print("Module could not be importet 'ImportError'" + str(e))

root = tk.Tk()
label = tk.Label(root, fg="green")
root.geometry("530x300")
root.resizable(0, 0)


def switch_advanced_using():
    global switch_advanced_using_var
    if switch_advanced_using_var == "False":
        switch_advanced_using_var = "True"
        advanced_using_button.config(text="✓")
    else:
        switch_advanced_using_var = "False"
        advanced_using_button.config(text="")


def switch_playlist_same_quality():
    global switch_playlist_same_quality_var
    if switch_playlist_same_quality_var == "False":
        switch_playlist_same_quality_var = "True"
        playlist_same_quality.config(text="✓")
    else:
        switch_playlist_same_quality_var = "False"
        playlist_same_quality.config(text="")


def func_to_settings():
    options.place_forget()

    c2.place_forget()
    c1.place_forget()
    dropdown_mp_.place_forget()
    settings_button.config(image=icon_back)
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
    settings_button.config(image=icon_settings)
    text_title.place(x=37, y=217)
    hidden_text.place(x=37, y=239)
    download_button.place(x=400, y=212)
    audio_dropdown.place(x=280, y=100)
    video_playlist_dropdown.place(x=430, y=100)
    if playlist_dropdown.get() == "Playlist" and switch_playlist_same_quality_var == "False":
        playlist_forward_button.place(x=449, y=147)
        playlist_backwards_button.place(x=400, y=147)

    settings_language.place_forget()
    bg_dropdown.place_forget()
    advanced_using_button.place_forget()
    playlist_same_quality.place_forget()
    c3.place_forget()

    save_data()


def set_bg_and_image(image__):
    os.chdir("..")
    try:
        os.chdir("data")
    except FileNotFoundError:
        os.makedirs("data")
        os.chdir("data")
    global image_, language_dict

    image_ = PhotoImage(file=str(image__) + ".png")
    c1.create_image(0, 0, image=image_)

    c1.create_text(60, 29, text=language_dict[cur_l][1], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(60, 63, text=language_dict[cur_l][2], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(60, 115, text=language_dict[cur_l][3], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(245, 115, text=language_dict[cur_l][4], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c1.create_text(396, 115, text="Type:", font=('Comic Sans MS', 10, 'normal'), fill="white")

    c2.create_image(0, 0, image=image_)

    c2.create_text(60, 29, text=language_dict[cur_l][1], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(60, 63, text=language_dict[cur_l][2], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(60, 115, text=language_dict[cur_l][3], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(83, 164, text=language_dict[cur_l][5], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(245, 115, text=language_dict[cur_l][4], font=('Comic Sans MS', 10, 'normal'), fill="white")
    c2.create_text(396, 115, text="Type:", font=('Comic Sans MS', 10, 'normal'), fill="white")


language_dict = {"English": ["Youtube to mp3/mp4 converter", "Video Link:", "File Name:", "Choose Format:", "Audio:",
                             "Choose Pixel Quality:", "Language:", "Background:", "Advanced Using:",
                             "Error: URL-Not Found", "Title:",
                             "DOWNLOADING - Youtube to mp3/mp4 converter                                         ",
                             "This Playlist is sadly not working :'(", "Error: Playlist URL-not Found",
                             "Error: You need to title your file!", "Error: File already exists!",
                             "Error: You have to set the pixel Quality!", "Error: Video has not the specified pixels!",
                             "Error: An Unknown Error occured!", "Success: Succesfully downloaded the Youtube Video!",
                             "Error: None", "resolution", "Settings", "Some settings are only updated\nafter a reboot!",
                             "Fast", "Fancy", "Download", "Status: Downloading...", "Error: No Playlist Given!",
                             "Error: End of the Playlist!", "Playlist same Quality:"],
                 "Deutsch": ["Youtube zu mp3 bzw. mp4 Convertierer", "Video Link:", "Datei Name:", "Wähle Format:",
                             "Audio:", "Wähle Pixel Qualität:", "Sprache:", "Hintergrund:", "mit cmd benutzen:",
                             "Fehler: URL nicht gefunden!", "Titel:",
                             "HERUNTERLADEN - Youtube zu mp3 bzw. mp4 Convertierer                            ",
                             "Diese Playlist funktioniert leider nicht :'(", "Fehler: Playlist URL night gefunden",
                             "Fehler: Du musst deiner Datei einen Namen geben!", "Fehler: Datei existiert bereits",
                             "Fehler: Du musst eine Qualität angeben!",
                             "Fehler: Video hat nicht die gewünschte Pixelanzahl!",
                             "Fehler: Ein unbekannter Fehler ist aufgetretten",
                             "Erfolg: Youtube Video erfolgreich heruntergelden", "Fehler: Keiner", "Qualität",
                             "Einstellungen", "Einige Einstellungen werden erst\nnach einem Neustart aktualisiert!",
                             "Schnell", "Schön", "Herunterladen", "Status: Herunterladen...",
                             "Fehler: Keine Playlist vorhanden!", "Fehler, Ende der Playlist!",
                             "Playlist selbe Qualität"],
                 }

try:
    os.chdir("data")
except FileNotFoundError:
    os.makedirs("data")
    os.chdir("data")

icon_settings = PhotoImage(file="settings_.png")
icon_back = PhotoImage(file="back.png")
icon_settingsBG = PhotoImage(file="SettingsBG.png")

playlist_forwards = PhotoImage(file="forward.png")
playlist_backwards = PhotoImage(file="backwards.png")

c1 = tk.Canvas(root, width=530, height=300)
c1.place(x=0, y=0)

c2 = tk.Canvas(root, width=530, height=300)
c3 = tk.Canvas(root, width=530, height=300)

c3.create_image(0, 0, image=icon_settingsBG)


def repair_data():
    print("Invalid data detected! Reseting data...")
    with open("data.txt", "w") as file:
        file.write("English;Bubbles;False;True")  # standard


advanced_using_button = tk.Button(root, text='', height=1, width=2, border=5, command=switch_advanced_using)
playlist_same_quality = tk.Button(root, text='', height=1, width=2, border=5, command=switch_playlist_same_quality)

set_bg = StringVar()
set_language = StringVar()
playlist_lst = []

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
        command_line = user_data[2]
        switch_advanced_using_var = user_data[2]
        if switch_advanced_using_var == "True":
            advanced_using_button.config(text="✓")

        switch_playlist_same_quality_var = user_data[3]
        if switch_playlist_same_quality_var == "True":
            playlist_same_quality.config(text="✓")

        set_language.set(str(user_data[0]))
        cur_l = str(user_data[0])

        set_bg.set(str(user_data[1]))
        set_bg_and_image(str(user_data[1]))

root.title(language_dict[cur_l][0])
c3.create_text(52, 29, text=language_dict[cur_l][6], font=('Comic Sans MS', 12, 'normal'), fill="white")
c3.create_text(60, 63, text=language_dict[cur_l][7], font=('Comic Sans MS', 12, 'normal'), fill="white")
c3.create_text(80, 97, text=language_dict[cur_l][8], font=('Comic Sans MS', 12, 'normal'), fill="white")
c3.create_text(95, 131, text=language_dict[cur_l][30], font=('Comic Sans MS', 12, 'normal'), fill="white")
c3.create_text(130, 260, text=language_dict[cur_l][23], font=('Comic Sans MS', 12, 'normal'), fill="white")

if command_line == "False" and win32installed:
    hide = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(hide, win32con.SW_HIDE)


def valid_link(link):  # function to check validity of the link

    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(link) and e.IE_NAME != 'generic':
            return True
    return False


def get_resolutions(link):
    yt = YouTube(link)
    lst, return_lst, final_return_lst = [], [], ["144p-fast"]
    download_button.place(x=400, y=212)

    resolution = yt.streams.filter(adaptive=True)
    for a in resolution:
        splited = str(a).split(" ")
        lst_elemts = ""
        for b in splited:
            if b.startswith("res") or b.startswith("fps"):
                for c in b:
                    if c in "0123456789":
                        lst_elemts += c
                lst_elemts += "p"
                for c in splited[splited.index(b) + 1]:
                    if c in "0123456789":
                        lst_elemts += c
                break
        lst.append(lst_elemts)
    for d in lst[::-1]:
        if d not in return_lst and d != "" and d[0] != "p" and str(d + "-fast") not in return_lst:
            if d[:3] in ["360", "720"]:
                return_lst.append(d + "-fast")
            else:
                return_lst.append(d)
    last_ = "p"
    for e in return_lst:
        if last_[:last_.find("p")] != e[:e.find("p")]:
            if e.startswith("720p"):
                try:
                    if int(e[-7:-5]) > 30:
                        final_return_lst.append("720p30-fast")
                    else:
                        final_return_lst.append("720p" + checkForNumber(e[-7:-5]) + "-fast")
                except Exception as err:
                    print("An Error occured - Some details (skipping video and continue downloading): ", err, "\n\n",
                          "E:", e, " FinalReturnList:", final_return_lst, "_last", last_)
            else:
                final_return_lst.append(e)
        last_ = e

    return final_return_lst, yt.title


counter_playlist = 0
playlist_last = ""


def display_options(*event):
    global lst_formats, resolutions, playlist_dropdown, counter_playlist, playlist_lst, playlist_formats, playlist_dropdown, playlist_last
    if link.get() == "":
        hidden_text.config(text=language_dict[cur_l][20])
        text_title.config(text=language_dict[cur_l][10])
        return
    if playlist_dropdown.get() == "Playlist":
        if playlist_last != link.get() or playlist_lst == []:
            text_title.config(text=language_dict[cur_l][10])
            playlist_lst = Playlist(link.get()).video_urls
            try:
                playlist_formats = [
                    {"Format": "mp3", "Audio": language_dict[cur_l][24], "Pixel": language_dict[cur_l][21]} for _ in
                    range(len(playlist_lst))]
            except KeyError:
                hidden_text.config(text=language_dict[cur_l][9])
                return
            counter_playlist = 0
            playlist_last = link.get()
            # formate zurücksetzen
            setIngameFormat()

    valid = valid_link(link.get())  # check the validity of link
    if not valid:
        hidden_text.config(text=language_dict[cur_l][9])
        print("Loading Video/Audio Failed! Error: URL-Not Found 404")
        return

    hidden_text.config(text=language_dict[cur_l][20])
    if playlist_dropdown.get() == "Playlist":
        url = playlist_lst[counter_playlist]
    else:
        url = link.get()
        options.set(language_dict[cur_l][21])

    ydl_opts = {}
    resolutions = []
    lst_formats = []

    if "list" in url:
        url = url.split("&list")[0]
    print(url)

    video_data = get_resolutions(url)

    if playlist_dropdown.get() == "Video":
        text_title.config(text=f'{language_dict[cur_l][10]} {video_data[1][:41]}')
    else:
        text_title.config(
            text=f'{language_dict[cur_l][10]} {video_data[1][:33]} - {counter_playlist + 1} / {len(playlist_lst)}')

    options['values'] = video_data[0]  # sets combobox values to available resolutions


def combine_audio(outname, fps=25):
    name_lst = [setname() + "_temp.mp3", setname() + "_temp.mp4"]
    my_clip = mpe.VideoFileClip(name_lst[1])
    audio_background = mpe.AudioFileClip(name_lst[0])
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)


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


settings_ = True
mp3_mp4_var__ = "mp3"


def func_settings():
    global settings_
    if settings_ == True:
        settings_ = False
        func_to_settings()
    else:
        settings_ = True
        func_back()


def setname():
    global name, mp3_mp4
    name2 = str(name.get())
    if name2 == "":
        return
    else:
        if name2[-4:] == ".mp3" and str(mp3_mp4.get()) == "mp3" or name2[-4:] == ".mp4" and str(mp3_mp4.get()) == "mp4":
            return name2[:-4]

        else:
            return name2


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
        root.after(15, download_yt_video_mp4)
        hidden_text.config(text=language_dict[cur_l][27] + " " * 45)
        download_button.place_forget()
        root.after(100, set_pixel_back)
    else:
        if name.get() == "":
            hidden_text.config(text=language_dict[cur_l][14])
            return
        try:
            setPlaylistFormat()
        except NameError:
            hidden_text.config(text=language_dict[cur_l][13])
            return
        download_button.place_forget()
        root.after(15, prepare_playlist_download)
        hidden_text.config(text=language_dict[cur_l][27] + " 1/" + str(len(playlist_lst)) + " " * 30)


orig_name = "None"


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
        hidden_text.config(text=language_dict[cur_l][15])
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
        if switch_playlist_same_quality_var == "False":
            download_yt_video_mp4(playlist_lst[playlist_index], playlist_formats[playlist_index]["Format"],
                                playlist_formats[playlist_index]["Audio"], playlist_formats[playlist_index]["Pixel"][
                                                                            :playlist_formats[playlist_index]["Pixel"].find(
                                                                                "p") + 1],
                                playlist_formats[playlist_index]["Pixel"])
        else:
            try:
                download_yt_video_mp4(playlist_lst[playlist_index], playlist_formats[0]["Format"],
                                    playlist_formats[0]["Audio"], playlist_formats[0]["Pixel"][
                                                                                :playlist_formats[0][
                                                                                    "Pixel"].find(
                                                                                    "p") + 1],
                                    playlist_formats[0]["Pixel"])
            except Exception as err:
                tempQuality = get_resolutions(playlist_lst[playlist_index])[0][-1]
                download_yt_video_mp4(playlist_lst[playlist_index], playlist_formats[0]["Format"],
                                    playlist_formats[0]["Audio"], tempQuality[
                                                                    :tempQuality.find(
                                                                        "p") + 1],
                                    tempQuality)
        hidden_text.config(
            text=language_dict[cur_l][27] + " " + str(playlist_index + 2) + "/" + str(len(playlist_lst)) + " " * 30)
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            root.after(50, continue_downloading)
        else:
            hidden_text.config(
                text=language_dict[cur_l][27] + " " + str(len(playlist_lst)) + "/" + str(len(playlist_lst)) + " " * 30)
            name.set(orig_name)
            set_pixel_back()
            hidden_text.config(text=language_dict[cur_l][19])
            os.chdir("..")
            return
    except Exception:
        print("Video is age restricted! Skipping!")
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            root.after(50, continue_downloading)


def download_yt_video_mp4(*args):
    if args == ():
        global link, mp3_mp4, fast_fancy
        format_ = option_lst.get()[:option_lst.get().find("p") + 1]
        format_2 = option_lst.get()
        _link, _mp3_mp4, _fast_fancy = link.get(), mp3_mp4.get(), fast_fancy.get()
    else:
        _link = args[0]
        _mp3_mp4 = args[1]
        _fast_fancy = args[2]
        format_ = args[3]
        format_2 = args[4]
    print(format_, format_2)

    root.title(language_dict[cur_l][11])
    print("Downloading...")

    if "list" in _link:
        _link = _link.split("&list")[0]
    print("Downloading audio... " + _link)
    if _mp3_mp4 == "mp4":
        try:
            yt = YouTube(_link)
        except Exception as err:
            hidden_text.config(text=language_dict[cur_l][9])
            root.title(language_dict[cur_l][0])
            print("Download Failed! Err:", str(err))
            raise "Unsupported Quality Error"
        if setname() == None:
            hidden_text.config(text=language_dict[cur_l][14])
            root.title(language_dict[cur_l][0])
            print("Download Failed! Err: No filename set!")
            return
        else:
            if (setname() + ".mp4") in os.listdir():
                hidden_text.config(text=language_dict[cur_l][15])
                root.title(language_dict[cur_l][0])
                print("Download Failed! Err: File already exists!")
                return
            try:
                print("DOWNLOADING with format: " + format_)
                if option_lst.get() == "resolution":
                    root.title(language_dict[cur_l][0])
                    hidden_text.config(text=language_dict[cur_l][16])
                    print("Download Failed! Err: No pixel Quality set!")
                    return
                if format_.startswith("360p") or format_.startswith("720p"):
                    yt.streams.filter(file_extension="mp4", res=format_).first().download(filename=setname() + ".mp4")
                    hidden_text.config(text=language_dict[cur_l][19])
                    root.title(language_dict[cur_l][0])
                    return
                elif format_2.startswith("144p-"):
                    yt.streams.filter().first().download(filename=setname() + ".mp4")
                    hidden_text.config(text=language_dict[cur_l][19])
                    root.title(language_dict[cur_l][0])
                    return
                else:
                    if _fast_fancy == language_dict[cur_l][24]:
                        yt.streams.filter(only_audio=True).first().download(filename=setname() + "_temp.mp3")
                    else:
                        ydl_opts2 = {'format': '140', 'outtmpl': setname() + ".m4a"}
                        for _ in range(10):
                            try:
                                with youtube_dl.YoutubeDL(ydl_opts2) as ydl2:
                                    ydl2.download([_link])
                            except Exception:
                                print("An Error occurred! (403 Forbidden) Retrying:", _)
                                continue
                            else:
                                os.rename(setname() + ".m4a", setname() + "_temp.mp3")
                                break

                    yt.streams.filter(file_extension="mp4", res=format_).first().download(
                        filename=setname() + "_temp.mp4")
                    # print(option_lst.get()[option_lst.get().find("p")+1:])

                    combine_audio(setname() + ".mp4", int(format_2[format_2.find("p") + 1:]))

                    os.system('del "' + setname() + '_temp.mp3"')
                    os.system('del "' + setname() + '_temp.mp4"')

            except AttributeError as err:
                print("Failed to download with 'pytube', trying with 'youtube-dl' now!")
                try:
                    ydl_opts = {'format': "mp4[height=" + format_[:-1] + "]", 'outtmpl': setname() + "_temp.mp4"}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([_link])
                    combine_audio(setname() + ".mp4", int(format_2[format_2.find("p") + 1:]))

                    os.system('del "' + setname() + '_temp.mp3"')
                    os.system('del "' + setname() + '_temp.mp4"')
                except Exception as err2:
                    try:
                        os.system('del "' + setname() + '_temp.mp3"')
                    except Exception as err:
                        print("Error occurred twice :) -> ", err)
                    hidden_text.config(text=language_dict[cur_l][17])
                    root.title(language_dict[cur_l][0])
                    print("Download Failed! Err:", str(err) + ",", str(err2))
                    print("If in Playlist download Queue, Retrying...")
                    raise "Unsupported Quality Error"
    else:
        try:
            yt = YouTube(_link)
        except Exception as err:
            hidden_text.config(text=language_dict[cur_l][9])
            root.title(language_dict[cur_l][0])
            print("Download Failed! Err:", str(err))
            return
        if setname() == None:
            hidden_text.config(text=language_dict[cur_l][14])
            root.title(language_dict[cur_l][0])
            print("Download Failed! Err: No filename set!")
            return
        else:
            if (setname() + ".mp3") in os.listdir():
                hidden_text.config(text=language_dict[cur_l][15])
                root.title(language_dict[cur_l][0])
                print("Download Failed! Err: File already exists!")
                return
            if _fast_fancy == language_dict[cur_l][24]:
                yt.streams.filter(only_audio=True).first().download(filename=setname() + ".mp3")
            else:
                ydl_opts2 = {'format': '140', 'outtmpl': setname() + ".m4a"}
                for _ in range(10):
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts2) as ydl2:
                            ydl2.download([_link])
                    except Exception:
                        print("An Error occurred! (403 Forbidden) Retrying:", _)
                        continue
                    else:
                        final_name = ""
                        for a in setname():
                            if a not in '\\/:*?<>|"':
                                final_name += a
                        os.rename(setname() + ".m4a", final_name + ".mp3")
                        break
        print("Download Complete")
    hidden_text.config(text=language_dict[cur_l][19])
    root.title(language_dict[cur_l][0])


def set_pixel_back():
    options.set(language_dict[cur_l][21])
    download_button.place(x=400, y=212)


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


def forwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        hidden_text.config(text=language_dict[cur_l][28])
    if playlist_lst == []:
        hidden_text.config(text=language_dict[cur_l][28])
        return
    if counter_playlist != len(playlist_lst) - 1:
        counter_playlist += 1
    else:
        hidden_text.config(text=language_dict[cur_l][29])
        return
    setIngameFormat()


def backwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        hidden_text.config(text=language_dict[cur_l][28])
    if playlist_lst == []:
        hidden_text.config(text=language_dict[cur_l][28])
        return
    if counter_playlist != 0:
        counter_playlist -= 1
    else:
        hidden_text.config(text=language_dict[cur_l][29])
        return
    setIngameFormat()


def change_playlist_vid(var):
    if var == "Playlist" and switch_playlist_same_quality_var == "False":
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


def checkForNumber(numberString):
    newNumber = ""

    for c in numberString:
        if c.isdigit():
            newNumber += c

    return newNumber

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

download_button = tk.Button(root, text=language_dict[cur_l][26], height=3, width=11, border=5, command=prepare_download)
download_button.place(x=400, y=212)

hidden_text = tk.Label(root, text=language_dict[cur_l][20], fg="black", font=('Comic Sans MS', 10, 'normal'),
                       highlightthickness=3)
hidden_text.place(x=37, y=239)

text_fps = tk.Label(root, text="Fps:", fg="black", font=('calibre', 10, 'normal'), highlightthickness=3)

fast_fancy = StringVar()
fast_fancy.set(language_dict[cur_l][24])
audio_dropdown = OptionMenu(root, fast_fancy, language_dict[cur_l][24], language_dict[cur_l][25])
audio_dropdown.place(x=280, y=100)

option_lst = StringVar()
link.trace('w', display_options)
option_lst.set(language_dict[cur_l][21])
options = ttk.Combobox(root, textvariable=option_lst, state="readonly", width=14)

text_title = tk.Label(root, text=language_dict[cur_l][10], fg="black", font=('Comic Sans MS', 8, 'normal'),
                      highlightthickness=3)
text_title.place(x=37, y=217)

settings_button = tk.Button(root, text='', height=35, width=32, border=5, command=func_settings, image=icon_settings)
settings_button.place(x=484, y=2)

settings_language = OptionMenu(root, set_language, "English", "Deutsch")

bg_dropdown = OptionMenu(root, set_bg, "Bubbles", "Hexagon", "Rose", "Plants", "Settings", command=set_bg_and_image)

playlist_dropdown = StringVar()
playlist_dropdown.set("Video")
video_playlist_dropdown = OptionMenu(root, playlist_dropdown, "Video", "Playlist", command=change_playlist_vid)
video_playlist_dropdown.place(x=430, y=100)

playlist_forward_button = tk.Button(root, text='', height=35, width=32, border=5, command=forwards_playlist,
                                    image=playlist_forwards)
playlist_backwards_button = tk.Button(root, text='', height=35, width=32, border=5, command=backwards_playlist,
                                      image=playlist_backwards)

root.mainloop()
