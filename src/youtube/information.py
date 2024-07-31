import youtube_dl
from pytube import YouTube

from src.main import gui_handler
from src.utils import utils


def valid_link(link):  # function to check validity of the link

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
                    quality = utils.checkForNumber(e[-7:-5])
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



