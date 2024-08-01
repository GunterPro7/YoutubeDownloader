from tkinter import StringVar

import youtube_dl
from pytubefix import YouTube

from src.gunterpro7.utils import audio_merger
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
    lst, return_lst, final_return_lst = [], [], ["144p-fast"]

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
                    error("An Error occured - Some details (skipping video and continue downloading): ", str(err), "\n\n",
                          "E:", e, " FinalReturnList:", str(final_return_lst), "_last", last_)
            else:
                final_return_lst.append(e)
        last_ = e

    return final_return_lst, yt.title


def download_yt_video_mp4(_link, _mp3_mp4, _fast_fancy, format_, format_2, name: StringVar) -> str:
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
                if format_.startswith("360p") or format_.startswith("720p"):
                    yt.streams.filter(file_extension="mp4", res=format_).first().download(filename=setname(name, _mp3_mp4) + ".mp4")
                    return language.get_idx(19)
                elif format_2.startswith("144p-"):
                    yt.streams.filter().first().download(filename=setname(name, _mp3_mp4) + ".mp4")
                    return language.get_idx(19)
                else:
                    if _fast_fancy == language.get_idx(24):
                        yt.streams.filter(only_audio=True).first().download(filename=setname(name, _mp3_mp4) + "_temp.mp3")
                    else:
                        ydl_opts2 = {'format': '140', 'outtmpl': setname(name, _mp3_mp4) + ".m4a"}
                        for _ in range(10):
                            try:
                                with youtube_dl.YoutubeDL(ydl_opts2) as ydl2:
                                    ydl2.download([_link])
                            except Exception:
                                error("An Error occurred! (403 Forbidden) Retrying:", str(_))
                                continue
                            else:
                                os.rename(setname(name, _mp3_mp4) + ".m4a", setname(name, _mp3_mp4) + "_temp.mp3")
                                break

                    yt.streams.filter(file_extension="mp4", res=format_).first().download(
                        filename=setname(name, _mp3_mp4) + "_temp.mp4")
                    # log(option_lst.get()[option_lst.get().find("p")+1:])

                    audio_merger.combine_audio(setname(name, _mp3_mp4) + ".mp4", name, _mp3_mp4, fps=int(format_2[format_2.find("p") + 1:]))

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
            if _fast_fancy == language.get_idx(24):
                yt.streams.filter(only_audio=True).first().download(filename=setname(name, _mp3_mp4) + ".mp3")
            else:
                ydl_opts2 = {'format': '140', 'outtmpl': setname(name, _mp3_mp4) + ".m4a"}
                for _ in range(10):
                    try:
                        with youtube_dl.YoutubeDL(ydl_opts2) as ydl2:
                            ydl2.download([_link])
                    except Exception:
                        error("An Error occurred! (403 Forbidden) Retrying:", str(_))
                        continue
                    else:
                        final_name = ""
                        for a in setname(name, _mp3_mp4):
                            if a not in '\\/:*?<>|"':
                                final_name += a
                        os.rename(setname(name, _mp3_mp4) + ".m4a", final_name + ".mp3")
                        break
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
