import gui_handler
from src.main import config, downloader


def __main__():
    # Setup
    gui_handler.__before_main__()
    config.__main__()
    gui_handler.__main__()

    # Run Gui
    downloader.test()
    gui_handler.__run__()



__main__()