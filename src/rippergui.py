from __future__ import unicode_literals

import re
import tkinter as tk
import tkinter.filedialog as filediag
import tkinter.font as tkfont
from functools import partial

from config import *
from src.data import pd
from src.logs import logging as log


def download_check(urlfile):
    inputs = []

    url = urlfile[0].get('1.0', tk.END).strip()
    inputs.extend(url.split('\n'))

    file = urlfile[1].get()
    if os.path.exists(file):
        with open(file, 'r') as file:
            inputs.extend((file.strip() for file in file.readlines()))

    urls = []
    re_url = re.compile(
        r'^((http|https)://)[-a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)$')
    for link in inputs:
        if re_url.search(link):
            urls.append(link)
            log.info(f"ADDING: {link}")
        else:
            log.info(f"IGNORING: {link}")

    win = tk.Toplevel()
    win.geometry("150x80")
    win.minsize(220, 100)
    win.maxsize(220, 100)
    win.wm_title("Download")
    if len(urls) > 0:
        label = tk.Label(win, text=f"You will download {len(urls)} link{'s' if len(urls) != 1 else ''}", font=tkfont.Font(size=10, weight="normal"))
        label.pack(side=tk.TOP, pady=15)
        close = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        close.pack(side=tk.RIGHT, pady=15, padx=28)
        confirm = tk.Button(win, text="Confirm", font=tkfont.Font(size=10, weight="bold"), command=partial(download, urls))
        confirm.pack(side=tk.LEFT, pady=15, padx=28)
    else:
        label = tk.Label(win, text=f"No links found", font=tkfont.Font(size=10, weight="normal"))
        label.pack(side=tk.TOP, pady=15)
        close = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        close.pack(pady=15, padx=28)


def download(urls):
    log.info(f"DOWNLOADING: {urls}")


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


def browse_directory(obj):
    directory = filediag.askdirectory()
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
                ('', '*.xml'),
                ('', '*.xls'),
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
        obj.set(f".../{os.path.basename(os.path.abspath(file.name))}")
        pd.config['songs_file'] = os.path.abspath(file.name)
        var.set(os.path.abspath(file.name))


def shift_focus(obj):
    obj.focus()


def update_url_paragraph_height(frame, url_paragraph, *args):
    main_frame_width = frame.winfo_width()
    main_frame_height = frame.winfo_height()
    url_paragraph_width = int((main_frame_width-RESOLUTION_X)/6 + 45)
    url_paragraph_height = int((main_frame_height-RESOLUTION_Y)/14 + 7)
    url_paragraph.config(width=url_paragraph_width, height=url_paragraph_height)


def open_localfiles():
    try:
        os.startfile(pd.appdata)
    except Exception:
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(180, 100)
        win.maxsize(180, 100)
        win.wm_title("Alert")
        l = tk.Label(win, text="AppData directory not found... This should never happen")
        l.pack(side=tk.TOP, pady=15)
        b = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        b.pack(side=tk.BOTTOM, pady=15, ipadx=6, ipady=4)


def open_downloads():
    try:
        os.startfile(pd.config['download_path'])
    except Exception:
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(180, 100)
        win.maxsize(180, 100)
        win.wm_title("Alert")
        l = tk.Label(win, text="Downloads directory not found")
        l.pack(side=tk.TOP, pady=15)
        b = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        b.pack(side=tk.BOTTOM, pady=15, ipadx=6, ipady=4)


def open_logs():
    pass


class RipperGUI(tk.Tk):

    def select_reset(self):
        log.info(f"Container selected {self.video_container.get()}")
        self.video_container.set("🎬")
        self.audio_container.set("🎵")

    def select_video(self, *args):
        video = self.video_container.get()
        if video in ("🎬", "🎵"):
            video = self.download_container.get()
        self.download_container.set(video)
        pd.config['download_container'] = video
        self.select_reset()

    def select_audio(self, *args):
        audio = self.audio_container.get()
        if audio in ("🎬", "🎵"):
            audio = self.download_container.get()
        self.download_container.set(audio)
        pd.config['download_container'] = audio
        self.select_reset()

    class FileLabelPlaceholder(tk.Frame):
        def __init__(self, parent=None, placeholder="None", textvariable=tk.StringVar, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.label = tk.Label(self, text=placeholder)
            self.label.pack(side=tk.LEFT)
            self.placeholder = placeholder
            self.textvariable = textvariable
            self.set(placeholder)
            self.hyperlink = tk.Label(self,
                text="✖️",
                fg="red",
                cursor="hand2")
            self.hyperlink.bind("<Button-1>", self.reset)

        def set(self, text):
            if text == self.placeholder:
                self.label.config(text=text, fg="grey")
            else:
                self.label.config(text=text, fg="black")
                log.debug(f"Song file added '{text}'")
                self.add_reset()

        def add_reset(self):
            self.hyperlink.pack(side=tk.RIGHT)

        def remove_reset(self):
            self.hyperlink.forget()
            self.textvariable.set("")

        def reset(self, event):
            log.debug("Song file removed")
            self.set(self.placeholder)
            self.remove_reset()

    class TextPlaceholder(tk.Text):
        def __init__(self, parent=None, placeholder="Type into here", phcolor="grey", *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.placeholder = placeholder
            self.placeholder_color = phcolor
            self.bind("<FocusIn>", self.focus_hide)
            self.bind("<FocusOut>", self.unfocus_show)
            self.unfocus_show()

        def focus_hide(self, *args):
            if self.get("1.0", "end-1c") == self.placeholder:
                self.delete("1.0", tk.END)
                self.config(foreground="black")

        def unfocus_show(self, *args):
            if self.get("1.0", "end-1c") == "":
                log.debug(f"'{self.placeholder}' TextPlaceholder displayed")
                self.insert("1.0", self.placeholder)
                self.config(foreground=self.placeholder_color)

    def run(self):
        log.info("GUI loop started")
        self.mainloop()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_strvar = tk.StringVar(self, pd.config['download_path'])
        self.video_container = tk.StringVar(self, "🎬")
        self.audio_container = tk.StringVar(self, "🎵")
        self.download_container = tk.StringVar(self, pd.config['download_container'])

        self.title_font = tkfont.Font(family="Yu Gothic", size=14, weight="bold")
        self.main_icon = tk.PhotoImage(file='assets\\obli-ripper-icon.png')

        self.geometry(f"{RESOLUTION_X}x{RESOLUTION_Y}")
        self.minsize(RESOLUTION_X, 414)
        self.maxsize(RESOLUTION_X*3, 2160)
        self.title(f"{VERSION} | {APP_NAME}")
        self.iconphoto(True, self.main_icon)
        self.config(background="#27263D")

        main_frame = tk.Frame(self,
            width=400)
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

        if pd.config['download_path'] != "":
            self.download_strvar.set(pd.config['download_path'])
        path_entry = tk.Entry(path_frame, textvariable=self.download_strvar, width=30)
        path_entry.pack(side=tk.LEFT)
        path_entry.bind("<Return>", lambda event: shift_focus(self))
        path_entry.bind("<FocusOut>", lambda event: validate_path(path_entry))

        browse_button = tk.Button(path_frame, text="🗀", cursor="hand2", command=partial(browse_directory, path_entry))
        browse_button.pack(side=tk.RIGHT)

# CONTENT FRAME
        content_frame1 = tk.Frame(main_frame)
        content_frame1.pack(padx=10, fill=tk.BOTH)
        content_frame2 = tk.Frame(main_frame)
        content_frame2.pack(padx=10, fill=tk.BOTH)
        content_frame3 = tk.Frame(main_frame)
        content_frame3.pack(padx=10, pady=10, fill=tk.BOTH)
        content_frame4 = tk.Frame(main_frame)
        content_frame4.pack(padx=10, fill=tk.BOTH)
        frame1_label = tk.Label(content_frame2, text="Enter link(s) or Select a premade file")
        frame1_label.pack(side=tk.TOP)

# URL PARAGRAPH
        url_frame = tk.Frame(content_frame2)
        url_frame.pack(side=tk.LEFT)
        url_paragraph = self.TextPlaceholder(url_frame, placeholder="https://...", height=7, width=45, wrap=tk.CHAR, font=tkfont.Font(size=8))
        url_paragraph.pack(side=tk.LEFT)
        self.bind("<Configure>", partial(update_url_paragraph_height, self, url_paragraph))
        url_scrollbar = tk.Scrollbar(url_frame, command=url_paragraph.yview, orient=tk.VERTICAL)
        url_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        url_paragraph['yscrollcommand'] = url_scrollbar.set

# SONGS FILE
        songs_frame = tk.Frame(content_frame2)
        songs_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
        songs_file = tk.StringVar(self)
        songs_filelabel = self.FileLabelPlaceholder(content_frame1, placeholder="No file", textvariable=songs_file)
        songs_filelabel.pack(side=tk.TOP)
        songs_button = tk.Button(songs_frame, text="🗍", cursor="hand2", command=partial(browse_file, songs_filelabel, songs_file), width=4)
        songs_button.pack(side=tk.TOP, ipadx=10)
        songs_label = tk.Label(songs_frame, text="Import list")
        songs_label.pack(side=tk.BOTTOM)

# CONTAINERS
        container_label = tk.Label(content_frame3, text="Output file type:  ")
        container_label.pack(side=tk.LEFT)
        containers_frame = tk.Frame(content_frame3)
        containers_frame.pack(side=tk.LEFT, pady=10)
        containers_label = tk.Label(containers_frame, textvariable=self.download_container, font=tkfont.Font(size=10, weight="normal"))
        containers_label.pack(side=tk.RIGHT, padx=8)

        video_containers_button = tk.OptionMenu(containers_frame, self.video_container, "🎬", *pd.config['video_containers'], command=self.select_video)
        video_containers_button.pack(side=tk.LEFT)
        audio_containers_button = tk.OptionMenu(containers_frame, self.audio_container, "🎵", *pd.config['audio_containers'], command=self.select_audio)
        audio_containers_button.pack(side=tk.LEFT)

# DOWNLOAD
        localfiles_button = tk.Button(content_frame4, text="🔧", width=5, height=2, font=tkfont.Font(size=11), command=open_localfiles)
        localfiles_button.pack(side=tk.LEFT)

        downloads_button = tk.Button(content_frame4, text="📂", width=5, height=2, font=tkfont.Font(size=11), command=open_downloads)
        downloads_button.pack(side=tk.LEFT)

        download_button = tk.Button(content_frame4,
            text="Download",
            command=partial(download_check, (url_paragraph, songs_file)),
            font=tkfont.Font(size=18),
            cursor="hand2",
            width=14,
            height=1)
        download_button.pack(side=tk.LEFT, pady=10)

        logs_button = tk.Button(content_frame4, text="📰", width=5, height=2, font=tkfont.Font(size=11), command=open_logs)
        logs_button.pack(side=tk.LEFT)

        log.info("GUI created")
