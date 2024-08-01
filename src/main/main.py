import gui_handler
from src.logger import logger
from src.logger.logger import *
from src.main import config


def __main__():
    # Init Logger
    logger.__init__()
    log("Starting YoutubeToMp3...")

    # Setup
    gui_handler.__main__()
    config.__main__()
    gui_handler.__setup__()

    # Run Gui
    gui_handler.__run__()


__main__()
