import os


class ProgramFilesNotFoundError(Exception):
    pass


def get_appdata_path():
    if os.name == 'nt':
        appdata_path = os.getenv('APPDATA')
        appdata_path = os.path.dirname(appdata_path)
        appdata_path = os.path.join(appdata_path, 'LocalLow')
    else:
        appdata_path = os.path.expanduser('~/.config')
    appdata_folder = os.path.join(appdata_path, NAME, APP_NAME)
    os.makedirs(appdata_folder, exist_ok=True)
    return appdata_folder


def get_programdata_path():
    if os.name == 'nt':
        program_data_path = os.environ.get('ProgramData')
    else:
        program_data_path = '/var/lib'
    program_data_path = os.path.join(program_data_path, NAME, APP_NAME)
    if not os.path.exists(program_data_path):
        raise ProgramFilesNotFoundError("No program data found")
    return program_data_path


def get_programfiles_path():
    if os.name == 'nt':
        program_files_path = os.environ.get('ProgramFiles')
    else:
        program_files_path = '/usr/local/bin'
    program_files_path = os.path.join(program_files_path, NAME, APP_NAME)
    if not os.path.exists(program_files_path):
        raise ProgramFilesNotFoundError("No program files found")
    return program_files_path


NAME = "Oblivius"
APP_NAME = "Ripper"
VERSION = "V2.0"

APP_ICON = os.path.join(get_programfiles_path(), "assets", "256.png")
CONFIGURATION_FILE = "config.conf"
LOG_COUNT = 100

RESOLUTION_X = 420
RESOLUTION_Y = 470

##### DEFAULTS #####
DOWNLOAD_PATH = os.path.expanduser('~')
DEBUG_LEVEL = 10  # 10:DEBUG 20:INFO 30:WARN 40:ERROR 50:CRITICAL
DOWNLOAD_CONTAINER = "webm"
VIDEO_CONTAINERS = "avi", "mkv", "m4v", "mov", "mp4", "webm"
AUDIO_CONTAINERS = "aac", "flac", "mp3", "ogg", "wav", "opus"
SONGS_FILE = ""
OUTPUT_TEMPLATE = "[ripper] %(fulltitle)s.%(ext)s"


# TODO
# Reload config
# set clip time and duration