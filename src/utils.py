from __future__ import unicode_literals

import tkinter as tk
import tkinter.filedialog as filediag
import tkinter.font as tkfont
from datetime import datetime

from config import *
from src.data import pd
from src.logs import logging as log


def stamp_now():
    return datetime.utcnow().timestamp()


def validate_path(obj):
    path = obj.get()
    if os.path.isdir(path):
        obj.config(bg="white")
        pd.config['download_path'] = path
        pd.save_appdata()
        log.debug(f"Validated path '{path}'")
    else:
        obj.config(bg="yellow")
        log.debug(f"Failed path '{path}'")


def browse_directory(obj, initialdir=None):
    directory = filediag.askdirectory(initialdir=initialdir)
    if directory:
        obj.delete(0, tk.END)
        obj.insert(tk.END, directory)
        validate_path(obj)


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
        log.debug(f"Song file selected '{os.path.basename(path)}'")
        obj.set(f".../{os.path.basename(path)}")
        pd.config['songs_file'] = path
        var.set(path)


def shift_focus(obj):
    obj.focus()


def update_url_paragraph_dimensions(frame, url_paragraph, *args):
    main_frame_width = frame.winfo_width()
    main_frame_height = frame.winfo_height()
    url_paragraph_width = int((main_frame_width-RESOLUTION_X)/6 + 45)
    url_paragraph_height = int((main_frame_height-RESOLUTION_Y)/14 + 7)
    url_paragraph.config(width=url_paragraph_width, height=url_paragraph_height)


def open_localfiles():
    try:
        os.startfile(pd.appdata)
        log.info("Opened Local folder")
    except Exception:
        log.critical("Couldn't open Local folder")
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
        log.info("Opened Downloads folder")
    except Exception:
        log.warning("Couldn't open Downloads folder")
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(180, 100)
        win.maxsize(180, 100)
        win.wm_title("Alert")
        l = tk.Label(win, text="Downloads directory not found")
        l.pack(side=tk.TOP, pady=15)
        b = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        b.pack(side=tk.BOTTOM, pady=15, ipadx=6, ipady=4)
