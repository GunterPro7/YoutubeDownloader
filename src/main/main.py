import gui_handler
from src.main import config

def __main__():
    gui_handler.__before_main__()
    config.__main__()
    gui_handler.__main__()

    pass



__main__()