from src.logger import logger
from src.logger.logger import *
from src.main import config, gui_handler, module_handler


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

    # Check if all Modules are installed
    module_handler.__main__()

    # Setup
    gui_handler.__main__()
    config.__main__()
    gui_handler.__setup__()

    # Run Gui
    gui_handler.__run__()


__main__()
