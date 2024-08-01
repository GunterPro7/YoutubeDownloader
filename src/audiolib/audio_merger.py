import moviepy.editor as mpe
from src.utils import file_utils


def combine_audio(outname: str, fps=25):
    name_lst = [file_utils.setname() + "_temp.mp3", file_utils.setname() + "_temp.mp4"]
    my_clip = mpe.VideoFileClip(name_lst[1])
    audio_background = mpe.AudioFileClip(name_lst[0])
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname, fps=fps)
