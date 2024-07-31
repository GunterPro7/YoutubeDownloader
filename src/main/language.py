from typing import Dict, List

language_dict: Dict[str, List[str]] = {"English": ["Youtube to mp3/mp4 converter", "Video Link:", "File Name:", "Choose Format:", "Audio:",
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


last_language: str = "English"


def set_language(language: str) -> List[str]:
    global last_language, language_dict

    if language in language_dict.keys():
        last_language = language


def get_idx(index: int) -> str:
    return language_dict[last_language][index]
