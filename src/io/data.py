import ast
import os
import logging

import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as filediag

from src.config import (
    NAME,
    APP_NAME,
    DOWNLOAD_PATH,
    DOWNLOAD_CONTAINER,
    DEBUG_LEVEL,
    VIDEO_CONTAINERS,
    AUDIO_CONTAINERS,
    SONGS_FILE,
    OUTPUT_TEMPLATE,
    CONFIGURATION_FILE,
)

logger = logging.getLogger()


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
            "output_template": OUTPUT_TEMPLATE
        }

    def save_appdata(self):
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        config_input = ""
        for key, value in self.config.items():
            if value is None:
                continue
            if key == "debug_level":
                value = f"{value} ### 10debug 20info 30waring 40error 50critical"
            elif key == "output_template":
                value = f"{value} ### https://github.com/yt-dlp/yt-dlp#output-template"
            config_input += f"{key.upper()}={value}\n"

        with open(config_file, 'w') as file:
            file.write(config_input)
        logger.info(f"Configuration file SAVED '{config_file}'")

    def load_appdata(self):
        # CONFIGURATION
        config_file = os.path.join(self.appdata, CONFIGURATION_FILE)
        if os.path.isfile(config_file):
            logger.info(f"Configuration file LOADED '{config_file}'")
            with open(config_file, 'r') as file:
                lines = file.readlines()
            if len(lines) == 0:
                logger.info(f"Configuration empty")
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
                logger.info(f"CONFIG {key}={value}")
            return
        logger.info(f"Configuration file NOT FOUND")


def open_localfiles():
    try:
        os.startfile(pd.appdata)
        logger.info("Opened Local folder")
    except Exception:
        logger.critical("Couldn't open Local folder")
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(180, 100)
        win.maxsize(180, 100)
        win.wm_title("Alert")
        label = tk.Label(win, text="AppData directory not found... This should never happen")
        label.pack(side=tk.TOP, pady=15)
        close = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        close.pack(side=tk.BOTTOM, pady=15, ipadx=6, ipady=4)


def open_downloads():
    try:
        os.startfile(pd.config['download_path'])
        logger.info("Opened Downloads folder")
    except Exception:
        logger.warning("Couldn't open Downloads folder")
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(180, 100)
        win.maxsize(180, 100)
        win.wm_title("Alert")
        l = tk.Label(win, text="Downloads directory not found")
        l.pack(side=tk.TOP, pady=15)
        b = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        b.pack(side=tk.BOTTOM, pady=15, ipadx=6, ipady=4)


def validate_path(obj):
    path = obj.get()
    if os.path.isdir(path):
        obj.config(bg="white")
        pd.config['download_path'] = path
        pd.save_appdata()
        logger.debug(f"Validated path '{path}'")
    else:
        obj.config(bg="yellow")
        logger.debug(f"Failed path '{path}'")


def browse_directory(obj, initialdir=None):
    directory = filediag.askdirectory(initialdir=initialdir)
    if directory:
        obj.delete(0, tk.END)
        obj.insert(tk.END, directory)
        validate_path(obj)
        logger.debug(f"Validated directory '{directory}'")


def browse_file(obj, var):
    try:
        file = filediag.askopenfile(
            filetypes=[
                ('', '*.txt'),
                ('', '*.csv'),
                ('', '*.tsv'),
                ('', '*.json'),
                ('', '*.xml'),
                ('', '*.xls'),
                ('', '*.xlxs'),
                ('', '*.cfg'),
                ('', '*.pls'),
                ('', '*.cure'),
                ('', '*.lst'),
                ('', '*.'),
                ('All Files', '.*')
            ]
        )
    except FileNotFoundError:
        return
    if file:
        path = os.path.abspath(file.name)
        logger.debug(f"Song file selected '{os.path.basename(path)}'")
        obj.set(f".../{os.path.basename(path)}")
        pd.config['songs_file'] = path
        var.set(path)


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


pd = ProgramData()
