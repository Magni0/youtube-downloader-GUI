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
        self.ffmpeg_binary = ""
        self.binary = ""

        # "--embed-thumbnail",
        self.init_command()
        self.url = ""
        self.download_path = ""

        # options
        
        # audio
        self.audio_only = False
        self.audio_format = "mp3"
        self.audio_quality = 5

        # video
        self.video_format = ["-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4"]
        self.playlist = False

    def init_command(self):
        slash = '/' if self.os != 'Windows' else '\\'
        binaries_folder = pathlib.Path(pathlib.Path(os.path.abspath(__file__)).parent.parent, "binaries")

        if not self.binary or not self.ffmpeg_binary:
            self.binary = f"{binaries_folder}{slash}yt-dlp.exe"
            self.ffmpeg_binary = f"{binaries_folder}{slash}"
            if self.os == "Linux":
                self.binary = f"{binaries_folder}{slash}yt-dlp_linux"
                self.ffmpeg_binary = f"{binaries_folder}{slash}"
            elif self.os == "Darwin":
                self.binary = f"{binaries_folder}{slash}yt-dlp_macos"
                self.ffmpeg_binary = f"{binaries_folder}{slash}"

        self.command: list = [self.binary,  "--add-metadata", "--prefer-free-formats"]
        self.postproccessing = ["--ffmpeg-location", self.ffmpeg_binary]

    def update_command(self, new_string: list):
        for i in new_string:
            self.command.append(str(i))

    def download(self):
        if not self.url or not self.download_path:
            raise ValueError("Missing url or download_path")
        
        if self.os == "Windows":
            self.command.append("--windows-filenames")
        else:
            self.command.append("--restrict-filenames")

        # file path
        self.update_command(["-P", f"'{self.download_path}'"])

        if self.audio_only:
            self.update_command(["-x", "--audio-format", self.audio_format])
            self.update_command(["--audio-quality", self.audio_quality])
        else:
            self.update_command([*self.video_format, "--embed-chapters"])

        if self.playlist:
            self.command.append("--yes-playlist")
        else:
            self.command.append("--no-playlist")

        # use portable postproccessing binary as it is not guaranteed that the device will have them
        # self.update_command(self.postproccessing)

        self.command.append(self.url)

        # preview command
        print(" ".join(self.command))
        
        # run command
        subprocess.call(self.command)

        # reset values for next download
        self.download_path = ""
        self.url = ""
        self.init_command()

        print(r"Done! ＼(＾O＾)／")