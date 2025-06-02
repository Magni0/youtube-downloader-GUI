"""Main file."""
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


@error_catch
def main():
    def download():
        yt_dlp = YTDownloader()
        yt_dlp.url = url.get()
        yt_dlp.audio_only = download_type.get()
        yt_dlp.playlist = playlist.get()
        yt_dlp.download_path = save_folder.get()

        yt_dlp.download()

    root = tk.Tk()
    root.title("YouTube Downloader")

    gui = GUI(root)

    download_type = gui.make_new_radio_button("Type", {"Video": False, "Audio": True}, row=1, column=0)
    playlist = gui.make_new_radio_button("Playlist", {"Yes": True, "No": False}, button=False, row=1, column=2)

    url = gui.make_new_entry(2, 0)

    save_folder = tk.StringVar()
    gui.make_file_explorer_button("Save Folder:", save_folder, 3, 0)
    gui.make_new_label(3, 1, save_folder)

    download_button = gui.make_new_button("Download", download, 4, 0)
    if not url.get() or not save_folder.get():
        download_button.state = "disabled"
    else:
        download_button.state = "normal"

    root.mainloop()


if __name__ == "__main__":
    main()