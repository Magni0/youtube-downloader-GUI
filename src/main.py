"""Main file."""
import os

import tkinter as tk
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


# @error_catch
def main():
    def download():
        yt_dlp = YTDownloader()
        yt_dlp.url = url.get()
        yt_dlp.audio_only = download_type.get() == "Audio"
        yt_dlp.playlist = playlist.get() == 1
        yt_dlp.download_path = save_folder.get()

        yt_dlp.download()

        url.set("")
        # save_folder.set("")


    os.environ["DISPLAY"] = ":0.0"

    root = tk.Tk()
    root.title("YouTube Downloader")

    gui = GUI(root)

    gui.make_new_label(1, 0, tk.StringVar(root, "Format:"))
    download_type = gui.make_new_listbox(options=["Video", "Audio"], row=1, column=1)
    gui.make_new_label(1, 2, tk.StringVar(root, "Playlist:"))
    playlist = gui.make_new_radio_button(False, {"Yes": True, "No": False}, row=1, column=3)

    gui.make_new_label(2, 0, tk.StringVar(root, "URL:"))
    url = gui.make_new_entry(2, 1)

    save_folder: tk.StringVar = gui.make_new_entry(3, 1, read_only=True)
    gui.make_file_explorer_button("Save Folder:", save_folder, 3, 0)

    download_button = gui.make_new_button("Download", download, 5, 0)

    root.mainloop()

    if not url.get() or not save_folder.get():
        download_button.state = "disabled"
    else:
        download_button.state = "normal"


if __name__ == "__main__":
    main()