"""Main file."""

import PySimpleGUI as sg
from modules.gui import GUI
from modules.downloader import YTDownloader

BUTTON_BLUE = "#082567"
SELECTED_COLOUR = (BUTTON_BLUE, "white")


def error_catch(func):
    def inner():
        try:
            func()
        except Exception:
            import traceback

            with open("youtube-downloader-error-log.txt", "w") as file:
                file.write(traceback.format_exc())
    
    return inner


@error_catch
def main():
    gui = GUI()
    yt_dlp = YTDownloader()
    window = gui.make_window()

    def get(key):
        return window[key].get()

    def update_button_theme(event: str, array: list):
        for k in array:
            window[k].update(button_color=sg.theme_button_color())
        window[event].update(button_color=SELECTED_COLOUR)

    # Defaults
    window[gui.VIDEO_AUDIO_OPTIONS[0]].update(button_color=SELECTED_COLOUR)
    window["playlist_No"].update(button_color=SELECTED_COLOUR)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'exit':
            break

        elif event == "url":
            if "playlist" in get("url"):
                active_radio_button = "playlist_Yes"
                update_button_theme(active_radio_button, [f"playlist_{i}" for i in gui.YES_NO_OPTIONS])

        # audio or video download
        elif event in gui.VIDEO_AUDIO_OPTIONS:
            update_button_theme(event, gui.VIDEO_AUDIO_OPTIONS)
            active_radio_button = event

            yt_dlp.audio_only = active_radio_button == "Audio"

            # hide/show video/audio specific elements
            for key in gui.AUDIO_ELEMENTS:
                window[key].update(visible=active_radio_button == "Audio")
            for key in gui.VIDEO_ELEMENTS:
                window[key].update(visible=active_radio_button == "Video")

        elif "playlist" in event:
            active_radio_button = event
            update_button_theme(active_radio_button, [f"playlist_{i}" for i in gui.YES_NO_OPTIONS])

            yt_dlp.playlist = active_radio_button == "playlist_Yes"

        elif event == "download":
            yt_dlp.url = get("url")
            yt_dlp.download_path = get("folder")

            if not yt_dlp.url or not yt_dlp.download_path:
                window["validate_error"].update(visible=True)
                continue

            window["validate_error"].update(visible=False)

            if yt_dlp.audio_only:
                yt_dlp.audio_format = values["audio_format_options"]

            yt_dlp.download()


if __name__ == "__main__":
    main()