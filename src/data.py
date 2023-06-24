import os
from config import *
import json
import ast
import logging
from src.utils import Singleton

def get_appdata_path():
    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        appdata_path = os.path.join(appdata_path, 'LocalLow')
    else:
        appdata_path = os.path.expanduser('~/.config')
    appdata_folder = os.path.join(appdata_path, NAME, APP_NAME)
    os.makedirs(appdata_folder, exist_ok=True)
    return appdata_folder


def save_path(directory):
    appdata_folder = get_appdata_path()
    appdata_file = os.path.join(appdata_folder, 'last_path.txt')

    with open(appdata_file, 'w') as file:
        file.write(directory)
    logging.info(f"AppData configuration file SAVED")


class ProgramData(metadata=Singleton):
    def __init__(self):
        self.appdata = get_appdata_path()
        self.config = {
            "download_path": "",
            "debug_level": DEBUG_LEVEL,
            "audio_file": AUDIO_FILE,
            "video_file": VIDEO_FILE,
        }

    def load_appdata(self):
        appdata_folder = get_appdata_path()
        appdata_file = os.path.join(appdata_folder, CONFIGURATION_FILE)
        if os.path.isfile(appdata_file):
            with open(appdata_file, 'r') as file:
                lines = file.readlines()
            if len(lines) == 0:
                logging.info(f"AppData configuration empty")
            else:
                logging.info(f"AppData configuration LOADED")
            for line in lines:
                conf = line.strip().split('###')[0]
                conf = conf.split('=')
                if not conf[0].strip().lower() in self.config:
                    continue
                self.config[conf[0].strip().lower()] = ast.literal_eval(conf[1].strip())
            return
        logging.info(f"AppData configuration file not found")
