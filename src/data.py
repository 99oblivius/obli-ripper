import ast

from config import *
from src.logs import logging as log


class ProgramData:
    def __init__(self):
        self.appdata = get_appdata_path()
        self.config = {
            "download_path": DOWNLOAD_PATH,
            "debug_level": DEBUG_LEVEL,
            "download_container": DOWNLOAD_CONTAINER,
            "video_containers": VIDEO_CONTAINERS,
            "audio_containers": AUDIO_CONTAINERS,
            "songs_file": SONGS_FILE,
        }

    def save_appdata(self):
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        config_input = ""
        for key, value in self.config.items():
            if value is not None:
                config_input += f"{key.upper()}={value}\n"

        with open(config_file, 'w') as file:
            file.write(config_input)
        log.info(f"Configuration file SAVED '{config_file}'")

    def load_appdata(self):
        # CONFIGURATION
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        if os.path.isfile(config_file):
            log.info(f"Configuration file LOADED '{config_file}'")
            with open(config_file, 'r') as file:
                lines = file.readlines()
            if len(lines) == 0:
                log.info(f"Configuration empty")
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
                log.info(f"CONFIG {key}={value}")
            return
        log.info(f"Configuration file NOT FOUND")


pd = ProgramData()
