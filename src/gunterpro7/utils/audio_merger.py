from tkinter import StringVar
from src.gunterpro7.logger.logger import *

import moviepy.editor as mpe


def combine_audio(outname: str, name: StringVar, mp3_mp4: StringVar, fps=25):
    log("Starting Merging Video and Audio to a single file")
    name_lst = [setname(name, mp3_mp4) + "_temp.mp3", setname(name, mp3_mp4) + "_temp.mp4"]
    my_clip = mpe.VideoFileClip(name_lst[1])
    audio_background = mpe.AudioFileClip(name_lst[0])
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
    log("Combining Done!")


def setname(name: StringVar, mp3_mp4):
    name = name.get()
    if name == "":
        return
    else:
        if name[-4:] == ".mp3" and str(mp3_mp4.get()) == "mp3" or name[-4:] == ".mp4" and str(mp3_mp4.get()) == "mp4":
            return name[:-4]
        else:
            return name
