"""Handles the GUI fields/layout."""

from tkinter.constants import HIDDEN
import PySimpleGUI as sg


class GUI:
    """https://github.com/PySimpleGUI/psgdemos/tree/main/psgdemos/demo_programs"""
    VIDEO_AUDIO_OPTIONS = ["Video", "Audio"]
    YES_NO_OPTIONS = ["Yes", "No"]

    AUDIO_ELEMENTS = ['audio_format_text', 'audio_format_options']
    VIDEO_ELEMENTS = []

    def button_options(array: list, prefix: str="") -> list:
        """Creates a button element list to be unpacked in the layout"""
        return [sg.Button(i, key=f"{prefix}{i}") for i in array]

    MAIN_LAYOUT = [
        [*button_options(VIDEO_AUDIO_OPTIONS), sg.Text("Playlist:"), *button_options(YES_NO_OPTIONS, prefix="playlist_")],
        [sg.Text("URL:"), sg.InputText(key="url")],
        [sg.Text("Save Folder:"), sg.InputText(key="folder", disabled=True), sg.FolderBrowse()],

        # [sg.Button],

        # Audio specific elements
        [sg.Text("Audio Format:", key='audio_format_text', visible=False), sg.OptionMenu(['aac', 'alac', 'flac', 'm4a', 'mp3', 'opus', 'vorbis', 'wav'], size=(15, 1), key="audio_format_options", default_value="mp3", visible=False)],

        # video specific elements

        # actions
        [sg.Button("Download", key="download"), sg.Button("Exit", key="exit")],
    ]

    def make_window(self) -> sg.Window:
        return sg.Window(
            'YouTube Downloader', 
            self.MAIN_LAYOUT, 
            grab_anywhere=True, 
            resizable=True, 
            margins=(0,0), 
            finalize=True, 
            keep_on_top=True
        )
