from pytube import YouTube
import os
import requests
from PIL import Image
from io import BytesIO
import threading
import customtkinter  # pip install customtkinter
from CTkMessagebox import CTkMessagebox  # pip install CTkMessagebox
import re
from class_settings import Settings_Window
from variables import APPNAME
import tkinterDnD  # pip install python-tkdnd
import json
import pywinstyles  # pip install pywinstyles


class PY_YT_DL(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
        self.title(f"{APPNAME}")

        frame = customtkinter.CTkFrame(master=self)
        frame.grid(row=0, column=0, pady=20, padx=20)

        header_image_ctk = customtkinter.CTkImage(dark_image=(Image.open("yt_logo.png")), size=(500, 150))
        header_image = customtkinter.CTkLabel(frame, text="")
        header_image.configure(image=header_image_ctk)
        header_image.grid(row=0, column=0, pady=2, padx=2)

        url_label = customtkinter.CTkLabel(frame, text="YouTube URL:", font=("bahnschrift", 20))
        url_label.grid(row=1, column=0, pady=20, padx=20)

        self.url_entry = customtkinter.CTkEntry(frame, width=500)
        self.url_entry.grid(row=2, column=0, pady=2, padx=2)

        mp3_mp4_label = customtkinter.CTkLabel(frame, text="MP4 / MP3", font=("bahnschrift", 20))
        mp3_mp4_label.grid(row=3, column=0, pady=20, padx=20)

        self.mp3_mp4_combobox_var = customtkinter.StringVar(value=["MP4", "MP3"])

        mp3_mp4_combobox = customtkinter.CTkComboBox(frame, variable=self.mp3_mp4_combobox_var, values=["MP4", "MP3"])
        mp3_mp4_combobox.grid(row=4, column=0, pady=2, padx=2)
        self.mp3_mp4_combobox_var.set("MP4")

        download_button = customtkinter.CTkButton(frame, text="Download", command=self.download_video)
        download_button.grid(row=5, column=0, pady=20, padx=20)

        load_button = customtkinter.CTkButton(frame, text="Load Infos", command=self.load_infos)
        load_button.grid(row=6, column=0)

        self.thumbnail_label = customtkinter.CTkLabel(frame, width=100, height=100, text="")
        self.thumbnail_label.grid(row=1, column=1, pady=2, padx=2)

        export_button = customtkinter.CTkButton(frame, text="Export as TXT", command=self.export_text)
        export_button.grid(row=3, column=1, pady=20, padx=20)

        self.info_textbox = customtkinter.CTkTextbox(frame, width=300, height=200)
        self.info_textbox.grid(row=2, column=1, pady=10, padx=10)

        self.progressbar_ctk = customtkinter.CTkProgressBar(frame, width=500)
        self.progressbar_ctk.grid(row=17, column=0, pady=10, padx=10)
        self.progressbar_ctk.set(0)

        self.progressbar_label = customtkinter.CTkLabel(frame, font=("bahnschrift", 15), text="")
        self.progressbar_label.grid(row=16, column=0, pady=2, padx=2)

        thumbnail_safe_button = customtkinter.CTkButton(frame, text="Safe Thumbnail", command=self.safe_thumbnail)
        thumbnail_safe_button.grid(row=4, column=1, pady=20, padx=20)

        self.settings_button = customtkinter.CTkButton(frame, text="Settings", command=self.open_toplevel)
        self.settings_button.grid(row=5, column=1)

    def open_toplevel(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = Settings_Window(self)
        else:
            self.toplevel_window.focus()

    def download_video(self):
        def msg_box_error():
            CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error\n"
                                                              f"Pleas enter a valid URL first.", icon="warning")

        def download():
            url = self.url_entry.get()
            if url == "":
                msg_box_error()
                return

            try:
                yt = YouTube(url, on_progress_callback=self.progressbar)
                title = yt.title

                info_text = (
                    f"Title:\n    {title}\n\n"
                    f"Length:\n    {yt.length} seconds\n\n"
                    f"Views:\n    {yt.views}\n\n"
                    f"Age restricted:\n    {'Yes' if yt.age_restricted else 'No'}\n\n"
                    f"Description:\n    {yt.description.replace('\n', '\n    ') if yt.description else 'N/A'}\n"

                )

                self.info_textbox.delete(1.0, customtkinter.END)
                self.info_textbox.insert(customtkinter.END, info_text)

                thumbnail_url = yt.thumbnail_url
                response = requests.get(thumbnail_url)
                image_data = response.content
                ctk_image = customtkinter.CTkImage(dark_image=Image.open(BytesIO(image_data)), size=(200, 200))
                self.thumbnail_label.configure(image=ctk_image)

                if self.mp3_mp4_combobox_var.get() == "MP4":
                    video = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
                        'resolution').desc().first()
                    download_path = os.path.join(os.getcwd(), 'downloads')
                    video.download(download_path)
                if self.mp3_mp4_combobox_var.get() == "MP3":
                    mp3_titel = title + ".mp3"
                    # Herunterladen der Audio-only-Datei als MP3
                    audio = yt.streams.filter(only_audio=False).first()
                    download_path = os.path.join(os.getcwd(), 'downloads')
                    audio.download(output_path=download_path, filename=mp3_titel)


            except Exception as e:
                print(e)

        thread = threading.Thread(target=download)
        thread.start()

    def progressbar(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_decimal = bytes_downloaded / total_size

        progress = min(1, max(0, progress_decimal))

        self.progressbar_ctk.set(progress)

        self.progressbar_label.configure(
            text=f"{bytes_downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB -- {progress * 100:.2f}% complete")
        self.title(
            f"{APPNAME} -- Downloading - {progress * 100:.2f}% complete - {bytes_downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB")

    def load_infos(self):
        def msg_box():
            CTkMessagebox(title=f"{APPNAME} - No valid URL", message=f"Pleas enter a valid URL.", icon="warning")

        url = self.url_entry.get()
        if url == "":
            msg_box()
        else:
            yt = YouTube(url)
            title = yt.title
            description = yt.description
            if description is None:
                description = "No description available."

            info_text = (
                f"Title:\n    {title}\n\n"
                f"Length:\n    {yt.length} seconds\n\n"
                f"Views:\n    {yt.views}\n\n"
                f"Age restricted:\n    {'Yes' if yt.age_restricted else 'No'}\n\n"
                f"Description:\n    {description.replace('\n', '\n    ')}\n"
            )

            self.info_textbox.delete(1.0, customtkinter.END)
            self.info_textbox.insert(customtkinter.END, info_text)

            thumbnail_url = yt.thumbnail_url
            response = requests.get(thumbnail_url)
            image_data = response.content
            ctk_image = customtkinter.CTkImage(dark_image=Image.open(BytesIO(image_data)), size=(200, 200))
            self.thumbnail_label.configure(image=ctk_image)

    def export_text(self):
        def msg_box_success():
            CTkMessagebox(title=f"{APPNAME} - Success", message=f"Successs\n"
                                                                f"Infos safed as {filename}.", icon="check")

        def msg_box_error():
            CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error\n"
                                                              f"Pleas load some infos first or download a video.")

        text = self.info_textbox.get(1.0, customtkinter.END)
        url = self.url_entry.get()

        if not text or not url:
            msg_box_error()
            return

        try:

            path = os.path.join(os.getcwd(), 'downloads')
            if not os.path.exists(path):
                os.makedirs(path)
            yt = YouTube(url)
            title = yt.title
            filename = f"{title}.txt"
            filepath = os.path.join(path, filename)
            with open(filepath, "w") as file:
                file.write(text)
            msg_box_success()
        except Exception as e:
            print(e)
            msg_box_error()

    def safe_filename(self, title):
        return re.sub(r'[^\w\s]', '_', title)

    def safe_thumbnail(self):
        def msg_box():
            CTkMessagebox(title=f"{APPNAME} - No valid URL", message=f"Please enter a valid URL.", icon="warning")

        def msg_box_success():
            CTkMessagebox(title=f"{APPNAME} - Success", message=f"Success\n"
                                                                f"Thumbnail safed as:\n"
                                                                f"{filename}")

        url = self.url_entry.get().strip()
        if not url:
            msg_box()
            return

        try:
            self.load_infos()
            path = os.path.join(os.getcwd(), 'downloads')

            if not os.path.exists(path):
                os.makedirs(path)

            yt = YouTube(url)
            title = yt.title
            thumbnail_url = yt.thumbnail_url
            response = requests.get(thumbnail_url)
            image_data = response.content
            filename = self.safe_filename(title) + ".png"
            filepath = os.path.join(path, filename)

            with open(filepath, "wb") as file:
                file.write(image_data)
                msg_box_success()

        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
