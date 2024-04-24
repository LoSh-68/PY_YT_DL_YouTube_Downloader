from pytube import YouTube
import os
import requests
from PIL import Image
from io import BytesIO
import threading
import customtkinter
from CTkMessagebox import CTkMessagebox
import re
from vars_defs import APPNAME, DOWNLOAD_FOLDER, JSON_DATA, SETTINGS_FILE, get_json_data
import pywinstyles
import tkinterDnD
import json
import winsound

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class PY_YT_DL(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
        self.title(f"{APPNAME}")
        self.wm_iconbitmap("PY_YT_DL.ico")
        self.set_settings()

        frame = customtkinter.CTkFrame(master=self)
        frame.grid(row=0, column=0, pady=20, padx=20)

        header_image_ctk = customtkinter.CTkImage(dark_image=(Image.open("yt_logo_light_blue.png")), size=(500, 150))
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

        download_button = customtkinter.CTkButton(frame, text="Download", command=self.download_video_audio)
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

    def download_video_audio(self):
        def msg_box_error():
            CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error\n"
                                                              f"Pleas enter a valid URL first.", icon="warning")

        def download():
            global use_oauth_bool, oauth_cache_bool, win_sound
            url = self.url_entry.get()

            if url == "":
                msg_box_error()
                return

            try:
                data = get_json_data()
                for item in data:
                    if item["id"] == 1:
                        use_oauth_bool = item["content"].lower() == "true"
                for item in data:
                    if item["id"] == 2:
                        oauth_cache_bool = item["content"].lower() == "true"
                for item in data:
                    if item["id"] == 3:
                        win_sound = item["content"]
                        break
                yt = YouTube(url, on_progress_callback=self.progressbar, use_oauth=use_oauth_bool,
                             allow_oauth_cache=oauth_cache_bool)
                title = yt.title
                print(use_oauth_bool)
                print(oauth_cache_bool)

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
                    download_path = os.path.join(os.getcwd(), DOWNLOAD_FOLDER)
                    file_path = os.path.join(download_path, title + ".mp4")

                    if os.path.exists(file_path):
                        CTkMessagebox(title=f"{APPNAME} - Info", message=f"Info\n{title}.mp4 already exists.")
                        return
                    if win_sound == "True":
                        video.download(download_path)
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    else:
                        video.download(download_path)

                if self.mp3_mp4_combobox_var.get() == "MP3":
                    mp3_titel = title + ".mp3"
                    audio = yt.streams.filter(only_audio=True).first()
                    download_path = os.path.join(os.getcwd(), DOWNLOAD_FOLDER)
                    file_path = os.path.join(download_path, title + ".mp3")

                    if os.path.exists(file_path):
                        CTkMessagebox(title=f"{APPNAME} - Info", message=f"Info\n{title}.mp3 already exists.")
                        return
                    if win_sound == "True":
                        audio.download(output_path=download_path, filename=mp3_titel)
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    else:
                        audio.download(output_path=download_path, filename=mp3_titel)

            except Exception as e:
                CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error:\n"
                                                                  f"{e}")
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
            print(f"Error: {e}")

    def set_settings(self):
        json_data = get_json_data()
        for item in json_data:
            if item["id"] == 4:
                set_theme = item["content"]
                break
        pywinstyles.apply_style(PY_YT_DL, style=f"{set_theme}")


class Settings_Window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.title(f"{APPNAME} - Settings")
        self.wm_iconbitmap("PY_YT_DL.ico")

        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=("bahnschrift", 30))
        self.settings_label.grid(row=0, column=0, pady=20, padx=20, columnspan=3)

        self.miscellaneous_settings_frame = customtkinter.CTkFrame(self, width=500, height=400, corner_radius=40)
        self.miscellaneous_settings_frame.grid(pady=20, padx=20, sticky="n", row=1, column=2)

        self.use_oauth_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="OAUTH:",
                                                      font=("bahnschrift", 15))
        self.use_oauth_label.grid(pady=20, padx=20, row=0, column=0)

        self.use_oauth_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame, values=["False", "True"],
                                                            corner_radius=20)
        self.use_oauth_combobox.grid(pady=20, padx=20, row=0, column=1)
        self.use_oauth_combobox.set("False")

        self.allow_oauth_cache_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="OAUTH Cache:",
                                                              font=("bahnschrift", 15))
        self.allow_oauth_cache_label.grid(pady=20, padx=20, row=1, column=0)

        self.allow_oauth_cache_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame,
                                                                    values=["False", "True"], corner_radius=20)
        self.allow_oauth_cache_combobox.grid(pady=20, padx=20, row=1, column=1)
        self.allow_oauth_cache_combobox.set("False")

        self.win_sound_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="Win Sound",
                                                      font=("bahnschrift", 15))
        self.win_sound_label.grid(pady=20, padx=20, row=2, column=0)

        self.win_sound_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame, values=["False", "True"],
                                                            corner_radius=20)
        self.win_sound_combobox.grid(pady=20, padx=20, row=2, column=1)
        self.win_sound_combobox.set("False")

        self.theme_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="Theme:",
                                                  font=("bahnschrift", 15))
        self.theme_label.grid(pady=20, padx=20, row=3, column=0)

        self.theme_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame, corner_radius=20,
                                                        values=["mica",
                                                                "acrylic",
                                                                "aero",
                                                                "transparent",
                                                                "optimised",
                                                                "win7",
                                                                "inverse",
                                                                "native",
                                                                "popup",
                                                                "dark",
                                                                "normal"])
        self.theme_combobox.grid(pady=20, padx=20, row=3, column=1)
        self.theme_combobox.set("dark")
        self.on_opening()

    def on_closing(self):
        data = get_json_data()
        oauth = self.use_oauth_combobox.get()
        oauth_cache = self.allow_oauth_cache_combobox.get()
        win_sound = self.win_sound_combobox.get()
        theme = self.theme_combobox.get()

        for item in data:

            if item["id"] == 1:
                item["content"] = oauth
            if item["id"] == 2:
                item["content"] = oauth_cache
            if item["id"] == 3:
                item["content"] = win_sound
            if item["id"] == 4:
                item["content"] = theme
                break
            with open(SETTINGS_FILE, "w") as json_file:
                json.dump(data, json_file, indent=4)
        self.change_theme()
        Settings_Window.destroy(self)

    def on_opening(self):
        print("hure")
        data = get_json_data()
        for item in data:

            if item["id"] == 1:
                oauth = item["content"]
            if item["id"] == 2:
                oauth_cache = item["content"]
            if item["id"] == 3:
                win_sound = item["content"]
            if item["id"] == 4:
                theme = item["content"]
                break
        self.use_oauth_combobox.set(f"{oauth}")
        self.allow_oauth_cache_combobox.set(oauth_cache)
        self.win_sound_combobox.set(win_sound)
        self.theme_combobox.set(theme)

    def change_theme(self):
        data = get_json_data()
        set_theme = self.theme_combobox.get()
        for item in data:
            if item["id"] == 4:
                item["content"] = set_theme
                break
        pywinstyles.apply_style(Settings_Window, style=f"{set_theme}")
        pywinstyles.apply_style(PY_YT_DL, style=f"{set_theme}")
        with open(SETTINGS_FILE, "w") as json_file:
            json.dump(data, json_file, indent=4)


if not os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(JSON_DATA, file, indent=4)

if __name__ == "__main__":
    PY_YT_DL = PY_YT_DL()
    PY_YT_DL.mainloop()
