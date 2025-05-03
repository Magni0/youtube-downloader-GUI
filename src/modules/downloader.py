"""This module manages the downloader (yt-dlp) API"""

import subprocess
import platform
import os
import pathlib


class YTDownloader:
    OPTION_COMMAND_MAP = {}

    """
        Example command line: ./yt-dlp.exe -x --audio-format mp3 -P "/Path/To/Download/Files/To" --restrict-filenames --yes-playlist --embed-thumbnail --add-metadata https://www.youtube.com/playlist?list=PLScfAP4C0m2zQZfS4MiOxZ8mXuSjGVeNp
        See full documentation at  https://github.com/yt-dlp/yt-dlp#readme
    """
    def __init__(self) -> None:
        self.os = platform.system()

        slash = '/' if self.os != 'Windows' else '\\'
        binaries_folder = pathlib.Path(pathlib.Path(os.path.abspath(__file__)).parent.parent, "binaries")

        if self.os == "Windows":
            binary = f"{binaries_folder}{slash}yt-dlp.exe"
        elif self.os == "Linux":
            binary = f"{binaries_folder}{slash}yt-dlp_linux"
        elif self.os == "Darwin":
            binary = f"{binaries_folder}{slash}yt-dlp_macos"

        self.command = f"{binary} --embed-thumbnail --add-metadata --prefer-free-formats"
        self.url = ""
        self.download_path = ""

        # options
        
        # audio
        self.audio_only = False
        self.audio_format = "mp3"
        self.audio_quality = 5

        # video
        self.video_format = " -f 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4] / bv*+ba/b'"
        self.playlist = False
    
    def update_command(self, new_string):
        self.command = self.command + new_string

    def download(self):
        if not self.url or not self.download_path:
            raise ValueError("Missing url or download_path")
        
        if self.os == "Windows":
            self.update_command(" --windows-filenames")
        else:
            self.update_command(" --restrict-filenames")

        self.update_command(f" -P {self.download_path.replace(' ', '-')}")

        if self.audio_only:
            self.update_command(f" -x --audio-format {self.audio_format}")
            self.update_command(f" --audio-quality {self.audio_quality}")
        else:
            self.update_command(self.video_format)
            self.update_command(" --embed-chapters")

        if self.playlist:
            self.update_command(f" --yes-playlist")

        self.update_command(" " + self.url)

        # run command \○/
        subprocess.call(self.command.split(" "))