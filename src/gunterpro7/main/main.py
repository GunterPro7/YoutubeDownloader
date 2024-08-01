import os

from src.gunterpro7.logger import logger
from src.gunterpro7.logger.logger import *
from src.gunterpro7.main import config, gui_handler


def __main__():
    # Init Logger
    logger.__init__()
    log("Starting YoutubeToMp3...")
    success("""
        __  __            __        __       ______      __  ___     _____    
        \\ \\/ /___  __  __/ /___  __/ /_  ___/_  __/___  /  |/  /___ |__  /    
         \\  / __ \\/ / / / __/ / / / __ \\/ _ \\/ / / __ \\/ /|_/ / __ \\ /_ <     
         / / /_/ / /_/ / /_/ /_/ / /_/ /  __/ / / /_/ / /  / / /_/ /__/ /     
        /_/\\____/\\__,_/\\__/\\__,_/_.___/\\___/_/  \\____/_/  /_/ .___/____/   
                                                           /_/
            __             ______            __            ____          _____
           / /_  __  __   / ____/_  ______  / /____  _____/ __ \\________/__  /
          / __ \\/ / / /  / / __/ / / / __ \\/ __/ _ \\/ ___/ /_/ / ___/ __ \\/ / 
         / /_/ / /_/ /  / /_/ / /_/ / / / / /_/  __/ /  / ____/ /  / /_/ / /  
        /_.___/\\__, /   \\____/\\__,_/_/ /_/\\__/\\___/_/  /_/   /_/   \\____/_/   
              /____/                                                          
        """)
    log("Working dir: " + str(os.getcwd()))

    # Setup
    gui_handler.__main__()
    config.__main__()
    gui_handler.__setup__()

    # Run Gui
    gui_handler.__run__()


__main__()
