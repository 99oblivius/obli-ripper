import os
from config import *
import json
import ast
import logging
from src.utils import Singleton


def get_appdata_path():
    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        appdata_path = os.path.dirname(appdata_path)
        appdata_path = os.path.join(appdata_path, 'LocalLow')
        print(f"get: {appdata_path}")
    else:
        appdata_path = os.path.expanduser('~/.config')
    appdata_folder = os.path.join(appdata_path, NAME, APP_NAME)
    os.makedirs(appdata_folder, exist_ok=True)
    return appdata_folder


class ProgramData:
    def __init__(self):
        self.appdata = get_appdata_path()
        self.config = {
            "download_path": "",
            "debug_level": DEBUG_LEVEL,
            "audio_file": AUDIO_FILE,
            "video_file": VIDEO_FILE,
        }

    def save_appdata(self):
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        config_input = ""
        for key, value in self.config.items():
            if value is not None and value != "":
                config_input += f"{key.upper()}={value}\n"

        with open(config_file, 'w') as file:
            file.write(config_input)
        logging.info(f"Configuration file SAVED '{config_file}'")

    def load_appdata(self):
        # CONFIGURATION
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        if os.path.isfile(config_file):
            logging.info(f"Configuration file LOADED '{config_file}'")
            with open(config_file, 'r') as file:
                lines = file.readlines()
            if len(lines) == 0:
                logging.info(f"Configuration empty")
            for line in lines:
                conf = line.strip().split('###')[0]
                conf = conf.split('=')
                key = conf[0].strip().lower()
                value = conf[1].strip()
                if key not in self.config or len(value) < 1:
                    continue
                try:
                    value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    pass
                finally:
                    self.config[key] = value
                logging.info(f"CONFIG {key}={value}")
            return
        logging.info(f"Configuration file NOT FOUND")


pd = ProgramData()
