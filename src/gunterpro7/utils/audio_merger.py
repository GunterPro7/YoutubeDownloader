import os
import subprocess
from tkinter import StringVar

from src.gunterpro7.logger.logger import *
from src.gunterpro7.main import config


def combine_audio(outname: str, name: StringVar, mp3_mp4: StringVar, fps: int = 25, bitrate: int = 128):
    def log(message: str):
        print(message)  # Replace with a proper logging function if needed

    log("Starting Merging Video and Audio to a single file")

    # Set filenames
    temp_audio: str = os.path.join(os.getcwd(), f"{setname(name, mp3_mp4)}_temp.mp3")
    temp_video: str = os.path.join(os.getcwd(), f"{setname(name, mp3_mp4)}_temp.mp4")

    ffmpeg_path = os.path.join(config.get_resources_path(), os.path.pardir, "ffmpeg")
    command = [
        ffmpeg_path,
        '-i', temp_video,  # Input video file
        '-i', temp_audio,  # Input audio file
        '-c:v', 'copy',  # Copy the video codec (no re-encoding)
        '-c:a', 'aac',  # Use AAC for audio codec
        '-b:a', str(bitrate) + "k",  # Set the audio bitrate
        '-strict', 'experimental',
        outname  # Output file
    ]
    subprocess.run(command)


def convert_webm_to_mp3(fileName: str, bitrate: int = 128):
    log("Starting converting Video webm to mp3 format")

    # ffmpeg -i input.webm -vn -ab 192k -ar 44100 -y output.mp3

    ffmpeg_path = os.path.join(config.get_resources_path(), os.path.pardir, "ffmpeg")
    command = [
        ffmpeg_path,
        "-i", fileName.replace(".mp3", ".webm"),
        "-vn",
        "-ab", str(bitrate) + "k",
        "-ar", "44100",
        "-y", fileName
    ]
    subprocess.run(command)

def setname(name: StringVar, mp3_mp4):
    name = name.get()
    if name == "":
        return
    else:
        if name[-4:] == ".mp3" and str(mp3_mp4.get()) == "mp3" or name[-4:] == ".mp4" and str(mp3_mp4.get()) == "mp4":
            return name[:-4]
        else:
            return name
