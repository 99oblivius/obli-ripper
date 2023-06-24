from __future__ import unicode_literals

import os
import tkinter as tk
import tkinter.filedialog as filediag
import tkinter.font as tkfont
import logging
from functools import partial

from src.data import ProgramData
from config import *


def validate_path(obj):
    path = obj.get()
    logging.debug(f"Validated path '{path}'")
    if os.path.isdir(path):
        obj.config(bg="white")
    else:
        obj.config(bg="yellow")


def browse_directory(obj):
    directory = filediag.askdirectory()
    if directory:
        obj.delete(0, tk.END)
        obj.insert(tk.END, directory)
        validate_path(obj)


def shift_focus(obj):
    obj.focus()


class RipperGUI(tk.Tk):

    def run(self):
        self.mainloop()
        logging.info("GUI loop started")

    def __init__(self):
        super().__init__()
        self.download_path = tk.StringVar(self, os.path.expanduser('~'))

        self.title_font = tkfont.Font(family="Yu Gothic", size=14, weight="bold")
        self.main_icon = tk.PhotoImage(file='assets\\obli-ripper-icon.png')

        self.geometry("420x720")
        self.minsize(420, 720)
        self.maxsize(420, 720)
        self.title(f"{VERSION} | {APP_NAME}")
        self.iconphoto(True, self.main_icon)
        self.config(background="#d9d0f2")

        main_frame = tk.Frame(self,
            width=400,
            highlightbackground="#222222",
            highlightthickness=1,
            highlightcolor="#24212b")
        main_frame.pack(padx=10, pady=20)

        # TITLE
        title_frame = tk.Frame(
            main_frame,
            width=400,
            highlightbackground="#222222",
            highlightthickness=1)
        title_frame.config()
        title_frame.pack(padx=10, pady=20)
        title_label = tk.Label(title_frame, text="YTDL Media content downloader", fg="#24212b", font=self.title_font, padx=20, pady=10)
        title_label.pack()

        # DOWNLOAD PATH
        path_frame = tk.Frame(title_frame)
        path_frame.pack(side=tk.LEFT, padx=10, pady=10)
        path_label = tk.Label(path_frame, text="Download path:")
        path_label.pack(side=tk.LEFT)
        path_entry = tk.Entry(path_frame, textvariable=self.download_path, width=30)
        path_entry.pack(side=tk.LEFT)
        browse_button = tk.Button(path_frame, text="🗀", command=partial(browse_directory, path_entry))
        browse_button.pack(side=tk.RIGHT)
        path_entry.bind("<Return>", lambda event: shift_focus(self))
        path_entry.bind("<FocusOut>", lambda event: validate_path(path_entry))

        logging.info("GUI created")

