import gui_handler
from src.logger import logger
from src.main import config


def __main__():
    # Setup
    logger.__init__()
    gui_handler.__main__()
    config.__main__()
    gui_handler.__setup__()

    logger.info("info")
    logger.log("log")
    logger.success("success")
    logger.warn("warn")
    logger.error("error")

    # Run Gui
    gui_handler.__run__()


__main__()
