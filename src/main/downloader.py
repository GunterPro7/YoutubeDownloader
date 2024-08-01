import os
import time

import youtube_dl
from pytube import YouTube, Playlist

from src.audiolib import audio_merger
from src.main import gui_handler, config, language
from src.utils.file_utils import setname
from src.utils.utils import checkForNumber

# Values (set later)
counter_playlist = 0
playlist_last = ""
orig_name = "None"


def valid_link(link: str):  # function to check validity of the link

    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(link) and e.IE_NAME != 'generic':
            return True
    return False


def get_resolutions(link):
    yt = YouTube(link)
    lst, return_lst, final_return_lst = [], [], ["144p-fast"]
    gui_handler.download_button.place(x=400, y=212)

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
                    quality = checkForNumber(e[-7:-5])
                    if int(quality) > 30:
                        final_return_lst.append("720p30-fast")
                    else:
                        final_return_lst.append("720p" + quality + "-fast")
                except Exception as err:
                    print("An Error occured - Some details (skipping video and continue downloading): ", err, "\n\n",
                          "E:", e, " FinalReturnList:", final_return_lst, "_last", last_)
            else:
                final_return_lst.append(e)
        last_ = e

    return final_return_lst, yt.title


def display_options(*event):
    global lst_formats, resolutions, playlist_dropdown, counter_playlist, playlist_lst, playlist_formats, playlist_dropdown, playlist_last
    if gui_handler.link.get() == "":
        gui_handler.hidden_text.config(text=language.get_idx(20))
        gui_handler.text_title.config(text=language.get_idx(10))
        return
    if playlist_dropdown.get() == "Playlist":
        if playlist_last != gui_handler.link.get() or playlist_lst == []:
            gui_handler.text_title.config(text=language.get_idx(10))
            playlist_lst = Playlist(gui_handler.link.get()).video_urls
            try:
                playlist_formats = [
                    {"Format": "mp3", "Audio": language.get_idx(24), "Pixel": language.get_idx(21)} for _ in
                    range(len(playlist_lst))]
            except KeyError:
                gui_handler.hidden_text.config(text=language.get_idx(9))
                return
            counter_playlist = 0
            playlist_last = gui_handler.link.get()
            # formate zurücksetzen
            setIngameFormat()

    valid = valid_link(gui_handler.link.get())  # check the validity of link
    if not valid:
        gui_handler.hidden_text.config(text=language.get_idx(9))
        print("Loading Video/Audio Failed! Error: URL-Not Found 404")
        return

    gui_handler.hidden_text.config(text=language.get_idx(20))
    if playlist_dropdown.get() == "Playlist":
        url = playlist_lst[counter_playlist]
    else:
        url = gui_handler.link.get()
        gui_handler.options.set(language.get_idx(21))

    ydl_opts = {}
    resolutions = []
    lst_formats = []

    if "list" in url:
        url = url.split("&list")[0]
    print(url)

    video_data = get_resolutions(url)

    if playlist_dropdown.get() == "Video":
        gui_handler.text_title.config(text=f'{language.get_idx(10)} {video_data[1][:41]}')
    else:
        gui_handler.text_title.config(
            text=f'{language.get_idx(10)} {video_data[1][:33]} - {counter_playlist + 1} / {len(playlist_lst)}')

    gui_handler.options['values'] = video_data[0]  # sets combobox values to available resolutions


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
        gui_handler.root.after(15, download_yt_video_mp4)
        gui_handler.hidden_text.config(text=language.get_idx(27) + " " * 45)
        gui_handler.download_button.place_forget()
        gui_handler.root.after(100, gui_handler.set_pixel_back)
    else:
        if gui_handler.name.get() == "":
            gui_handler.hidden_text.config(text=language.get_idx(14))
            return
        try:
            setPlaylistFormat()
        except NameError:
            gui_handler.hidden_text.config(text=language.get_idx(13))
            return
        gui_handler.download_button.place_forget()
        gui_handler.root.after(15, prepare_playlist_download)
        gui_handler.hidden_text.config(text=language.get_idx(27) + " 1/" + str(len(playlist_lst)) + " " * 30)


def prepare_playlist_download():
    global playlist_index, orig_name
    playlist_index = 0
    orig_name = gui_handler.name.get()
    print(orig_name)
    try:
        os.chdir(orig_name)
    except FileNotFoundError:
        os.makedirs(orig_name)
        os.chdir(orig_name)
    else:
        gui_handler.hidden_text.config(text=language.get_idx(15))
        return
    print("Downloading in directory --> " + os.getcwd())

    gui_handler.root.after(50, continue_downloading)


def continue_downloading():
    global playlist_lst, playlist_formats, playlist_index, orig_name
    try:
        prev_name = get_resolutions(playlist_lst[playlist_index])[1]
        gui_handler.download_button.place_forget()
        final_name = ""
        for a in prev_name:
            if a not in '\\/:*?<>|"':
                final_name += a

        gui_handler.name.set(final_name)
        if not config.switch_playlist_same_quality_var:
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
        gui_handler.hidden_text.config(
            text=language.get_idx(27) + " " + str(playlist_index + 2) + "/" + str(len(playlist_lst)) + " " * 30)
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            gui_handler.root.after(50, continue_downloading)
        else:
            gui_handler.hidden_text.config(
                text=language.get_idx(27) + " " + str(len(playlist_lst)) + "/" + str(len(playlist_lst)) + " " * 30)
            gui_handler.name.set(orig_name)
            gui_handler.set_pixel_back()
            gui_handler.hidden_text.config(text=language.get_idx(19))
            os.chdir("..")
            return
    except Exception:
        print("Video is age restricted! Skipping!")
        playlist_index += 1
        if playlist_index != len(playlist_lst):
            gui_handler.root.after(50, continue_downloading)


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

    gui_handler.root.title(language.get_idx(11))
    print("Downloading...")

    if "list" in _link:
        _link = _link.split("&list")[0]
    print("Downloading audio... " + _link)
    if _mp3_mp4 == "mp4":
        try:
            yt = YouTube(_link)
        except Exception as err:
            gui_handler.hidden_text.config(text=language.get_idx(9))
            gui_handler.root.title(language.get_idx(0))
            print("Download Failed! Err:", str(err))
            raise "Unsupported Quality Error"
        if setname() == None:
            gui_handler.hidden_text.config(text=language.get_idx(14))
            gui_handler.root.title(language.get_idx(0))
            print("Download Failed! Err: No filename set!")
            return
        else:
            if (setname() + ".mp4") in os.listdir():
                gui_handler.hidden_text.config(text=language.get_idx(15))
                gui_handler.root.title(language.get_idx(0))
                print("Download Failed! Err: File already exists!")
                return
            try:
                print("DOWNLOADING with format: " + format_)
                if option_lst.get() == "resolution":
                    gui_handler.root.title(language.get_idx(0))
                    gui_handler.hidden_text.config(text=language.get_idx(16))
                    print("Download Failed! Err: No pixel Quality set!")
                    return
                if format_.startswith("360p") or format_.startswith("720p"):
                    yt.streams.filter(file_extension="mp4", res=format_).first().download(filename=setname() + ".mp4")
                    gui_handler.hidden_text.config(text=language.get_idx(19))
                    gui_handler.root.title(language.get_idx(0))
                    return
                elif format_2.startswith("144p-"):
                    yt.streams.filter().first().download(filename=setname() + ".mp4")
                    gui_handler.hidden_text.config(text=language.get_idx(19))
                    gui_handler.root.title(language.get_idx(0))
                    return
                else:
                    if _fast_fancy == language.get_idx(24):
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

                    audio_merger.combine_audio(setname() + ".mp4", int(format_2[format_2.find("p") + 1:]))

                    os.system('del "' + setname() + '_temp.mp3"')
                    os.system('del "' + setname() + '_temp.mp4"')

            except AttributeError as err:
                print("Failed to download with 'pytube', trying with 'youtube-dl' now!")
                try:
                    ydl_opts = {'format': "mp4[height=" + format_[:-1] + "]", 'outtmpl': setname() + "_temp.mp4"}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([_link])
                    audio_merger.combine_audio(setname() + ".mp4", int(format_2[format_2.find("p") + 1:]))

                    os.system('del "' + setname() + '_temp.mp3"')
                    os.system('del "' + setname() + '_temp.mp4"')
                except Exception as err2:
                    try:
                        os.system('del "' + setname() + '_temp.mp3"')
                    except Exception as err:
                        print("Error occurred twice :) -> ", err)
                    gui_handler.hidden_text.config(text=language.get_idx(17))
                    gui_handler.root.title(language.get_idx(0))
                    print("Download Failed! Err:", str(err) + ",", str(err2))
                    print("If in Playlist download Queue, Retrying...")
                    raise "Unsupported Quality Error"
    else:
        try:
            yt = YouTube(_link)
        except Exception as err:
            gui_handler.hidden_text.config(text=language.get_idx(9))
            gui_handler.root.title(language.get_idx(0))
            print("Download Failed! Err:", str(err))
            return
        if setname() == None:
            gui_handler.hidden_text.config(text=language.get_idx(14))
            gui_handler.root.title(language.get_idx(0))
            print("Download Failed! Err: No filename set!")
            return
        else:
            if (setname() + ".mp3") in os.listdir():
                gui_handler.hidden_text.config(text=language.get_idx(15))
                gui_handler.root.title(language.get_idx(0))
                print("Download Failed! Err: File already exists!")
                return
            if _fast_fancy == language.get_idx(24):
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
    gui_handler.hidden_text.config(text=language.get_idx(19))
    gui_handler.root.title(language.get_idx(0))

def forwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        gui_handler.hidden_text.config(text=language.get_idx(28))
    if playlist_lst == []:
        gui_handler.hidden_text.config(text=language.get_idx(28))
        return
    if counter_playlist != len(playlist_lst) - 1:
        counter_playlist += 1
    else:
        gui_handler.hidden_text.config(text=language.get_idx(29))
        return
    setIngameFormat()


def backwards_playlist():
    global playlist_lst, counter_playlist
    try:
        setPlaylistFormat()
    except NameError:
        gui_handler.hidden_text.config(text=language.get_idx(28))
    if playlist_lst == []:
        gui_handler.hidden_text.config(text=language.get_idx(28))
        return
    if counter_playlist != 0:
        counter_playlist -= 1
    else:
        gui_handler.hidden_text.config(text=language.get_idx(29))
        return
    setIngameFormat()


def change_playlist_vid(var):
    if var == "Playlist" and not config.switch_playlist_same_quality_var:
        gui_handler.playlist_forward_button.place(x=449, y=147)
        gui_handler.playlist_backwards_button.place(x=400, y=147)
    else:
        gui_handler.playlist_forward_button.place_forget()
        gui_handler.playlist_backwards_button.place_forget()
    display_options()


def setIngameFormat():
    global playlist_formats
    if playlist_formats[counter_playlist]["Format"] == "mp4":
        gui_handler.options.place(x=160, y=155)

        gui_handler.c2.place(x=0, y=0)
        gui_handler.c1.place_forget()
        mp3_mp4.set("mp4")
    else:
        gui_handler.options.place_forget()

        gui_handler.c1.place(x=0, y=0)
        gui_handler.c2.place_forget()
        mp3_mp4.set("mp3")
    global fast_fancy, option_lst
    fast_fancy.set(playlist_formats[counter_playlist]["Audio"])
    option_lst.set(playlist_formats[counter_playlist]["Pixel"])
    display_options()


def setPlaylistFormat():
    global counter_playlist, playlist_formats, mp3_mp4, option_lst

    new_format_dict = {"Format": mp3_mp4.get(), "Audio": fast_fancy.get(), "Pixel": option_lst.get()}
    playlist_formats[counter_playlist] = new_format_dict


def test():
    return None