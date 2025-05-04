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

        binary = f"{binaries_folder}{slash}yt-dlp.exe"
        ffmpeg_binary = f"{binaries_folder}{slash}"
        if self.os == "Linux":
            binary = f"{binaries_folder}{slash}yt-dlp_linux"
            ffmpeg_binary = f"{binaries_folder}{slash}"
        elif self.os == "Darwin":
            binary = f"{binaries_folder}{slash}yt-dlp_macos"
            ffmpeg_binary = f"{binaries_folder}{slash}"

        # "--embed-thumbnail",
        self.command: list = [binary,  "--add-metadata", "--prefer-free-formats"]
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

        
        self.postproccessing = ["--ffmpeg-location", ffmpeg_binary]
    
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
        self.update_command(["-P", f"{self.download_path.replace(' ', '-')}"])

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

        print("Done! \○/")