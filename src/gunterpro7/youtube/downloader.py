from tkinter import StringVar

import yt_dlp as youtube_dl
from pytubefix import YouTube

from src.gunterpro7.utils import audio_merger, utils
from src.gunterpro7.logger.logger import *
from src.gunterpro7.main import language, gui_handler
from src.gunterpro7.utils.utils import checkForNumber


# function to check validity of the link
def valid_link(link: str) -> bool:
    extractors = youtube_dl.extractor.gen_extractors()
    for e in extractors:
        if e.suitable(link) and e.IE_NAME != 'generic':
            return True
    return False


def get_resolutions(link: str):
    yt = YouTube(link)
    lst, return_lst, final_return_lst, audio_list = [], [], [], []

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
            if b.startswith("abr"):
                audio_list.append(b.lstrip('abr="').rstrip('"'))
        lst.append(lst_elemts)
    for d in lst[::-1]:
        if d not in return_lst and d != "" and d[0] != "p" and str(d + "-fast") not in return_lst:
            return_lst.append(d)
    last_ = "p"
    for e in return_lst:
        if last_[:last_.find("p")] != e[:e.find("p")]:
            final_return_lst.append(e)
        last_ = e

    audio_list.sort(key=lambda x: int(x.replace('kbps', '')))
    return final_return_lst, yt.title, audio_list


def download_yt_video_mp4(_link, _mp3_mp4, _fast_fancy, format_, format_2, name: StringVar, audio_quality: StringVar) -> str:
    log("Formats: " + format_, format_2)
    log("Downloading (link: " + _link + ") ...")

    if "list" in _link:
        _link = _link.split("&list")[0]
    log("Downloading audio... " + _link)
    if _mp3_mp4 == "mp4":
        try:
            yt = YouTube(_link)
        except Exception as err:
            gui_handler.hidden_text.config(text=language.get_idx(9))
            gui_handler.root.title(language.get_idx(0))
            error("Download Failed! Err:", str(err))
            return language.get_idx(9)
        if setname(name, _mp3_mp4) == None:
            error("Download Failed! Err: No filename set!")
            return language.get_idx(14)
        else:
            if (setname(name, _mp3_mp4) + ".mp4") in os.listdir():
                error("Download Failed! Err: File already exists!")
                return language.get_idx(15)
            try:
                log("DOWNLOADING with format: " + format_)
                if format_2 == "resolution":
                    error("Download Failed! Err: No pixel Quality set!")
                    return language.get_idx(16)
                else:
                    yt.streams.filter(only_audio=True, abr=audio_quality.get()).first().download(filename=setname(name, _mp3_mp4) + "_temp.mp3")

                    yt.streams.filter(file_extension="mp4", res=format_).first().download(
                        filename=setname(name, _mp3_mp4) + "_temp.mp4")
                    # log(option_lst.get()[option_lst.get().find("p")+1:])

                    audio_merger.combine_audio(setname(name, _mp3_mp4) + ".mp4", name, _mp3_mp4, fps=int(format_2[format_2.find("p") + 1:]), bitrate=utils.to_int(audio_quality.get()))

                    log("Removing old audio and old movie file")
                    os.system('del "' + setname(name, _mp3_mp4) + '_temp.mp3"')
                    os.system('del "' + setname(name, _mp3_mp4) + '_temp.mp4"')

            except AttributeError as err:
                warn("Failed to download with 'pytube', trying with 'youtube-dl' now!")
                try:
                    ydl_opts = {'format': "mp4[height=" + format_[:-1] + "]", 'outtmpl': setname(name, _mp3_mp4) + "_temp.mp4"}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([_link])
                    audio_merger.combine_audio(setname(name, _mp3_mp4) + ".mp4", name, _mp3_mp4, int(format_2[format_2.find("p") + 1:]))

                    log("Removing old audio and old movie file")
                    os.system('del "' + setname(name, _mp3_mp4) + '_temp.mp3"')
                    os.system('del "' + setname(name, _mp3_mp4) + '_temp.mp4"')
                except Exception as err2:
                    try:
                        os.system('del "' + setname(name, _mp3_mp4) + '_temp.mp3"')
                    except Exception as err:
                        error("Error occurred twice :) -> ", str(err))
                    error("Download Failed! Err:", str(err) + ",", str(err2))
                    info("If in Playlist download Queue, Retrying...")
                    return language.get_idx(17)
    else:
        try:
            yt = YouTube(_link)
        except Exception as err:
            error("Download Failed! Err:", str(err))
            return language.get_idx(9)
        if setname(name, _mp3_mp4) == None:
            error("Download Failed! Err: No filename set!")
            return language.get_idx(14)
        else:
            if (setname(name, _mp3_mp4) + ".mp3") in os.listdir():
                error("Download Failed! Err: File already exists!")
                return language.get_idx(15)
            yt.streams.filter(only_audio=True, abr=audio_quality.get()).first().download(filename=setname(name, _mp3_mp4) + ".mp3")
        success("Download Complete: " + _link)
    return language.get_idx(19)


def setname(name, mp3_mp4):
    name2 = str(name.get())
    if name2 == "":
        return
    else:
        if name2[-4:] == ".mp3" and str(mp3_mp4.get()) == "mp3" or name2[-4:] == ".mp4" and str(mp3_mp4.get()) == "mp4":
            return name2[:-4]

        else:
            return name2
