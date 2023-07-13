from __future__ import unicode_literals

import logging
import re
import sys
import threading
import webbrowser
from functools import partial

import yt_dlp

from src.data import pd
from src.dependencies import rquirements_setup
from src.logs import MyLogger
from src.utils import *

logger = logging.getLogger()


class RipperException:
    def __init__(self, message="Error"):
        self.message = message
        self._error()

    def _error(self):
        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(220, 100)
        win.maxsize(220, 100)
        win.wm_title("Exception")
        label = tk.Label(win, text=f"Error: {self.message}", font=tkfont.Font(size=10, weight="bold"))
        label.pack(side=tk.TOP, pady=15)
        close = tk.Button(win, text="Close", font=tkfont.Font(size=10, weight="bold"), command=win.destroy)
        close.pack(pady=15, padx=28)


class RipperGUI(tk.Tk):
    class FunctionalButton(tk.Button):
        def __init__(self, parent=None, action=None, cursor="hand2", *args, **kwargs):
            super().__init__(parent, *args, cursor=cursor, **kwargs)
            self.bind("<ButtonRelease>", action)
            self.bind("<KeyRelease-space>", action)
            self.bind("<KeyRelease-Return>", action)

    class FileLabelPlaceholder(tk.Frame):
        def __init__(self, parent=None, placeholder="None", textvariable: tk.StringVar=None, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.label = tk.Label(self, text=placeholder)
            self.label.pack(side=tk.LEFT)
            self.placeholder = placeholder
            self.textvariable = textvariable
            self.hyperlink = tk.Label(self,
                text="✖️",
                fg="red",
                cursor="hand2")
            self.hyperlink.bind("<Button-1>", self.reset)

            if textvariable.get() == "": self.set(placeholder)
            else: self.set(textvariable.get())

        def set(self, text):
            if text == self.placeholder:
                self.label.config(text=text, fg="grey")
            else:
                self.label.config(text=text, fg="black")
                logger.debug(f"Song file added '{text}'")
                self.add_reset()

        def add_reset(self):
            self.hyperlink.pack(side=tk.RIGHT)

        def remove_reset(self):
            self.hyperlink.forget()
            self.textvariable.set("")
            pd.config['songs_file'] = ""

        def reset(self, event):
            logger.debug("Song file removed")
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
                logger.debug(f"'{self.placeholder}' TextPlaceholder displayed")
                self.insert("1.0", self.placeholder)
                self.config(foreground=self.placeholder_color)

    class ConsoleWindow(tk.Toplevel):
        class ConsoleRedirector:
            def __init__(self, text_widget, stream):
                self.text_widget = text_widget
                self.stream = stream

            def write(self, message):
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)

            def flush(self):
                pass

        def __init__(self, parent=None, *args, **kwargs):
            super().__init__(parent, *args, **kwargs)
            self.close_window()
            self.geometry("500x250")
            self.minsize(500, 170)
            self.title = "Console"

            self.console_title = tk.Label(self, text="Console Output", font=tkfont.Font(size=20))
            self.console_title.pack(side=tk.TOP, pady=5)

            self.console_frame = tk.Frame(self, bg="black")
            self.console_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            self.console_text = tk.Text(self.console_frame, wrap=tk.NONE, bg="black", fg="white", font='TkFixedFont')
            self.console_text.pack(fill=tk.BOTH, expand=True)

            sys.stdout = self.ConsoleRedirector(self.console_text, sys.stdout)
            sys.stderr = self.ConsoleRedirector(self.console_text, sys.stderr)

        def open_window(self):
            self.deiconify()

        def close_window(self):
            self.withdraw()

    def logs_toggle(self):
        if self.console_open:
            self.console_window.close_window()
        else:
            self.console_window.open_window()
        self.console_open = not self.console_open

    def download_check(self):
        inputs = []
        url = self.url_paragraph.get('1.0', tk.END).strip()
        inputs.extend(url.split('\n'))

        file = self.songs_file.get()
        if os.path.exists(file):
            with open(file, 'r') as file:
                inputs.extend((file.strip() for file in file.readlines()))

        re_url = re.compile(
            r'^((http|https)://)[-a-zA-Z0-9@:%._\+~#?&//=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%._\+~#?&//=]*)$')
        self.urls.clear()
        for link in inputs:
            match = re_url.search(link)
            if match:
                self.urls.append(match.group())
                logger.info(f"ADDING: {match.group()}")
            else:
                logger.debug(f"IGNORING: {link}")

        win = tk.Toplevel()
        win.geometry("150x80")
        win.minsize(220, 100)
        win.maxsize(220, 100)
        win.wm_title("Download")
        url_count = len(self.urls)

        def action_close(event):
            win.destroy()

        def action_confirm(event):
            if self.download_thread is None:
                self.threaded_download()
            win.destroy()

        close_button = self.FunctionalButton(win, text="Close", action=action_close, font=tkfont.Font(size=10, weight="bold"))

        if url_count > 0:
            accept_label = tk.Label(win,
                text=f"You will download {url_count} url{'s' if url_count != 1 else ''}",
                font=tkfont.Font(size=10, weight="normal"))
            accept_label.pack(side=tk.TOP, pady=15)

            confirm_button = self.FunctionalButton(win, action=action_confirm, text="Confirm", font=tkfont.Font(size=10, weight="bold"))
            confirm_button.pack(side=tk.LEFT, pady=15, padx=28)
            confirm_button.focus_set()
            close_button.pack(side=tk.RIGHT, pady=15, padx=28)
        else:
            logger.debug("No links found")
            empty_label = tk.Label(win, text=f"No links found", font=tkfont.Font(size=10, weight="normal"))
            empty_label.pack(side=tk.TOP, pady=15)
            empty_label.focus_set()
            close_button.pack(side=tk.BOTTOM, pady=15, padx=28)

    def threaded_download(self):
        self.download_thread = threading.Thread(target=self.download_function)
        logger.debug("Download thread starting")
        self.download_thread.start()

    def download_function(self):
        container = self.download_container.get()
        download_options = {
            "ignoreerrors": False,
            "live_from_start": True,
            "logger": MyLogger(),
            "ffmpeg_location": os.path.join(get_programfiles_path(), "bin"),
            "progress_hooks": [self.progress_hook],
            "postprocessor_hooks": [self.postprocessor_hook],
            "format-sort": 'ext',
            "outtmpl": pd.config['output_template']
        }
        if container in VIDEO_CONTAINERS:
            download_options.update({"format": f"bv*[ext={container}]+ba/b*[ext={container}]/bv*",
                "postprocessors": [
                    {"key": "FFmpegVideoRemuxer", "preferedformat": container}
                ]})
        elif container in AUDIO_CONTAINERS:
            download_options.update({"format": f"ba[ext=opus]/ba/b",
                "extract-audio": True,
                "postprocessors": [
                    {"key": "FFmpegExtractAudio", "preferredcodec": container}
                ]})

        links = '\n'.join(self.urls)
        logger.info(f"Downloading {container}:\n{links}")
        os.chdir(pd.config['download_path'])
        self.download_button.config(state=tk.DISABLED, cursor="heart")
        self.ytdl = yt_dlp.YoutubeDL(download_options)
        self.ytdl.download(self.urls)
        self.download_button.config(state=tk.ACTIVE, cursor="hand2")
        self.download_thread = None
        self.download_label.set("Download")

    def progress_hook(self, event):
        if event['status'] == 'finished':
            return
        now = stamp_now()
        if now > self.progress_stamp+0.5:
            if event['status'] == 'downloading':
                self.progress_stamp = now
                speed = event["_speed_str"]
                percentage = event["_percent_str"]
                if speed.strip().startswith("Unknown"): return
                self.download_label.set(f"{speed} {percentage} [{self.ytdl.count_progress}/{self.ytdl.total_count}]")
            else:
                self.download_label.set("Waiting")

    def postprocessor_hook(self, event):
        if event['status'] == 'finished':
            return
        now = stamp_now()
        if event['status'] == 'started':
            self.download_label.set(f"Processing [{self.ytdl.count_progress}/{self.ytdl.total_count}]")
        elif now > self.progress_stamp + 0.5 and event['status'] == 'processing':
            self.progress_stamp = now
            self.download_label.set(f"Processing Download")

    def select_reset(self):
        logger.info(f"Container selected {self.video_container.get()}")
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

    def run(self):
        logger.info("GUI loop started")
        self.mainloop()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.download_strvar = tk.StringVar(self, pd.config['download_path'])
        self.video_container = tk.StringVar(self, "🎬")
        self.audio_container = tk.StringVar(self, "🎵")
        self.download_container = tk.StringVar(self, pd.config['download_container'])
        self.songs_file = tk.StringVar(self, pd.config['songs_file'])

        self.title_font = tkfont.Font(family="Yu Gothic", size=14, weight="bold")
        self.main_icon = tk.PhotoImage(file=APP_ICON)

        self.geometry(f"{RESOLUTION_X}x{RESOLUTION_Y}")
        self.minsize(RESOLUTION_X, 414)
        self.maxsize(RESOLUTION_X*3, 2160)
        self.title(f"{VERSION} | {APP_NAME}")
        self.iconphoto(True, self.main_icon)
        self.config(background="#27263D")

        self.console_window = self.ConsoleWindow()
        self.progress_stamp = stamp_now()
        self.console_open = False
        self.url_paragraph = None
        self.download_button = None
        self.download_label = None

        self.urls = []
        self.download_thread = None
        self.ytdl = None

        main_frame = tk.Frame(self, width=400)
        main_frame.pack(padx=10, pady=20)

# TITLE
        title_frame = tk.Frame(
            main_frame,
            width=400,
            highlightbackground="#222222",
            highlightthickness=1)
        title_frame.config()
        title_frame.pack(padx=10, pady=20)
        title_label = tk.Label(title_frame, text="Media content downloader", fg="#24212b", font=self.title_font, padx=20)
        title_label.pack()
        supported_label = tk.Label(title_frame, text="Supported sites", fg="blue", cursor="hand2",font=("", 8, "underline"))
        supported_label.pack()
        supported_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md"))

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

        browse_button = self.FunctionalButton(path_frame, text="🗀", command=partial(browse_directory, path_entry, pd.config['download_path']))
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
        self.url_paragraph = self.TextPlaceholder(url_frame, placeholder="https://...", height=7, width=45, wrap=tk.CHAR, font=tkfont.Font(size=8))
        self.url_paragraph.pack(side=tk.LEFT)
        self.bind("<Configure>", partial(update_url_paragraph_dimensions, self, self.url_paragraph))
        url_scrollbar = tk.Scrollbar(url_frame, command=self.url_paragraph.yview, orient=tk.VERTICAL)
        url_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
        self.url_paragraph['yscrollcommand'] = url_scrollbar.set

# SONGS FILE
        songs_frame = tk.Frame(content_frame2)
        songs_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10)
        songs_filelabel = self.FileLabelPlaceholder(content_frame1, placeholder="No file", textvariable=self.songs_file)
        songs_filelabel.pack(side=tk.TOP)
        songs_button = self.FunctionalButton(songs_frame, text="🗍", command=partial(browse_file, songs_filelabel, self.songs_file), width=4)
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
        localfiles_button = self.FunctionalButton(content_frame4, text="🔧", width=5, height=2, font=tkfont.Font(size=11), command=open_localfiles)
        localfiles_button.pack(side=tk.LEFT)

        self.downloads_button = self.FunctionalButton(content_frame4, text="📂", width=5, height=2, font=tkfont.Font(size=11), command=open_downloads)
        self.downloads_button.pack(side=tk.LEFT)
        self.download_label = tk.StringVar(self, "Download")
        requirements = rquirements_setup()
        state = tk.ACTIVE if requirements else tk.DISABLED
        cursor = "hand2" if requirements else "question_arrow"
        text = self.download_label if requirements else tk.StringVar(self, "Dependencies missing")
        self.download_button = self.FunctionalButton(content_frame4,
            textvariable=text,
            command=partial(self.download_check),
            font=tkfont.Font(size=11),
            width=22,
            height=2,
            cursor=cursor,
            state=state)
        self.download_button.pack(side=tk.LEFT, pady=10)

        logs_button = self.FunctionalButton(content_frame4, text="📰", width=5, height=2, font=tkfont.Font(size=11), command=self.logs_toggle)
        logs_button.pack(side=tk.LEFT)

        logger.info("GUI created")
