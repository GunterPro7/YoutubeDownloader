import gui_handler
from src.main import config, downloader


def __main__():
    # Setup
    gui_handler.__main__()
    config.__main__()
    gui_handler.__setup__()

    # Run Gui
    gui_handler.__run__()



__main__()