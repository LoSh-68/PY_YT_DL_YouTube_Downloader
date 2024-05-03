import io
import pytube.helpers
from pytube import YouTube
import os
import requests
from PIL import Image
from io import BytesIO
import threading
import customtkinter
from CTkMessagebox import CTkMessagebox
from vars_defs import APPNAME, DOWNLOAD_FOLDER, JSON_DATA, SETTINGS_FILE, get_json_data, welcome_messsage, clear_console
import pywinstyles
import tkinterDnD
import json
import winsound
import psutil
from colorama import Fore, Back, Style
from images_base64 import PY_YT_DL_ICO_BASE64, YT_LOGO_LIGHT_BLUE_BASE64
import base64

customtkinter.set_ctk_parent_class(tkinterDnD.Tk)

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

prev_net_io = psutil.net_io_counters()

PY_YT_DL_ICO_BASE_64 = PY_YT_DL_ICO_BASE64
PY_YT_DL_ICO_BASE_64_DATA = base64.b64decode(PY_YT_DL_ICO_BASE_64)
PY_YT_DL_ICO_BASE_64_STREAM = io.BytesIO(PY_YT_DL_ICO_BASE_64_DATA)
PY_YT_DL_ICO_IMAGE = Image.open(PY_YT_DL_ICO_BASE_64_STREAM)
PY_YT_DL_ICO_IMAGE_TEMP_PATH = "TEMP_PY_YT_DL.ico"
PY_YT_DL_ICO_IMAGE.save(PY_YT_DL_ICO_IMAGE_TEMP_PATH)

PY_YT_DL_YT_LOGO_BASE_64 = YT_LOGO_LIGHT_BLUE_BASE64
PY_YT_DL_YT_LOGO_BASE_64_DATA = base64.b64decode(PY_YT_DL_YT_LOGO_BASE_64)
PY_YT_DL_YT_LOGO_BASE_64_STREAM = io.BytesIO(PY_YT_DL_YT_LOGO_BASE_64_DATA)
PY_YT_DL_YT_LOGO_IMAGE = Image.open(PY_YT_DL_YT_LOGO_BASE_64_STREAM)
PY_YT_DL_YT_LOGO_IMAGE_TEMP_PATH = "TEMP_YT_LOGO_LIGHT_BLUE.png"
PY_YT_DL_YT_LOGO_IMAGE.save(PY_YT_DL_YT_LOGO_IMAGE_TEMP_PATH)




class PY_YT_DL(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.toplevel_window = None
        self.title(f"{APPNAME}")
        self.wm_iconbitmap(PY_YT_DL_ICO_IMAGE_TEMP_PATH)
        os.remove(PY_YT_DL_ICO_IMAGE_TEMP_PATH)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.set_settings()
        welcome_messsage()

        frame = customtkinter.CTkFrame(master=self)
        frame.grid(row=0, column=0, pady=20, padx=20, columnspan=2)

        frame_url_progress = customtkinter.CTkFrame(master=self, corner_radius=30)
        frame_url_progress.grid(row=1, column=0, pady=20, padx=20)

        frame_download_load_infos = customtkinter.CTkFrame(master=self, corner_radius=30)
        frame_download_load_infos.grid(row=2, column=0, pady=20, padx=20)

        frame_titel_textbox = customtkinter.CTkFrame(master=self, corner_radius=30)
        frame_titel_textbox.grid(row=1, column=1, pady=20, padx=20)

        frame_option_buttons = customtkinter.CTkFrame(master=self, corner_radius=30)
        frame_option_buttons.grid(row=2, column=1, pady=20, padx=20)

        header_image_ctk = customtkinter.CTkImage(dark_image=(Image.open(PY_YT_DL_YT_LOGO_IMAGE_TEMP_PATH)), size=(500, 150))
        header_image = customtkinter.CTkLabel(frame, text="")
        header_image.configure(image=header_image_ctk)
        header_image.grid(row=0, column=0, pady=2, padx=2)
        os.remove(PY_YT_DL_YT_LOGO_IMAGE_TEMP_PATH)

        url_label = customtkinter.CTkLabel(frame_url_progress, text="YouTube URL:", font=("bahnschrift", 20))
        url_label.grid(row=1, column=0, pady=20, padx=20)

        self.url_entry = customtkinter.CTkEntry(frame_url_progress, width=700, font=("bahnschrift", 15))
        self.url_entry.grid(row=2, column=0, pady=20, padx=20)

        mp3_mp4_label = customtkinter.CTkLabel(frame_download_load_infos, text="Video==MP4 / Audio==MP3",
                                               font=("bahnschrift", 20))
        mp3_mp4_label.grid(row=3, column=0, pady=20, padx=20)

        self.mp3_mp4_combobox_var = customtkinter.StringVar(value=["MP4", "MP3"])

        mp3_mp4_combobox = customtkinter.CTkComboBox(frame_download_load_infos, variable=self.mp3_mp4_combobox_var,
                                                     values=["MP4", "MP3"])
        mp3_mp4_combobox.grid(row=4, column=0, pady=2, padx=2)
        self.mp3_mp4_combobox_var.set("MP4")

        self.download_button = customtkinter.CTkButton(frame_download_load_infos, text="⏬ Download",
                                                       command=self.download_video_audio)
        self.download_button.grid(row=5, column=0, pady=20, padx=20)

        self.load_button = customtkinter.CTkButton(frame_download_load_infos, text="🔄️ Load Infos",
                                                   command=self.load_infos)
        self.load_button.grid(row=6, column=0, pady=20, padx=20)

        self.thumbnail_label = customtkinter.CTkLabel(frame_titel_textbox, width=100, height=100, text="")
        self.thumbnail_label.grid(row=2, column=1, pady=2, padx=2)

        buttons_frame_label = customtkinter.CTkLabel(frame_option_buttons, text="Miscellaneous",
                                                     font=("bahnschrift", 20))
        buttons_frame_label.grid(row=0, column=0, pady=20, padx=20)

        export_button = customtkinter.CTkButton(frame_option_buttons, text="📝 Export info as TXT",
                                                command=self.export_text)
        export_button.grid(row=1, column=0, pady=10, padx=10)

        self.titel_label_text = customtkinter.CTkLabel(frame_titel_textbox, text="Titel:", font=("bahnschrift", 15))
        self.titel_label_text.grid(row=1, column=0, pady=20, padx=20)

        self.titel_label = customtkinter.CTkLabel(frame_titel_textbox, text="", font=("bahnschrift", 15))
        self.titel_label.grid(row=1, column=1, pady=20, padx=20)

        self.info_textbox_label = customtkinter.CTkLabel(frame_titel_textbox, text="Infos:", font=("bahnschrift", 15))
        self.info_textbox_label.grid(row=3, column=0, pady=20, padx=20)

        self.thumbnail_label_text = customtkinter.CTkLabel(frame_titel_textbox, text="Thumbnail:",
                                                           font=("bahnschrift", 15))
        self.thumbnail_label_text.grid(row=2, column=0, pady=20, padx=20)

        self.info_textbox = customtkinter.CTkTextbox(frame_titel_textbox, width=300, height=200)
        self.info_textbox.grid(row=3, column=1, pady=10, padx=10)

        self.progressbar_ctk = customtkinter.CTkProgressBar(frame_url_progress, width=500)
        self.progressbar_ctk.grid(row=17, column=0, pady=10, padx=10)
        self.progressbar_ctk.set(0)

        self.progressbar_label = customtkinter.CTkLabel(frame_url_progress, font=("bahnschrift", 15),
                                                        text="⬆️ Enter a YT or YT-Music URL and start downloading")
        self.progressbar_label.grid(row=16, column=0, pady=2, padx=2)

        thumbnail_safe_button = customtkinter.CTkButton(frame_option_buttons, text="🖼️Safe Thumbnail",
                                                        command=self.safe_thumbnail)
        thumbnail_safe_button.grid(row=2, column=0, pady=10, padx=10)

        self.settings_button = customtkinter.CTkButton(frame_option_buttons, text="⚙️ Settings",
                                                       command=self.open_toplevel)
        self.settings_button.grid(row=5, column=0, pady=10, padx=10)

        self.download_folder_button = customtkinter.CTkButton(frame_option_buttons, text="📂 Open Download Folder",
                                                              command=self.open_download_folder)
        self.download_folder_button.grid(pady=10, padx=10, row=4, column=0)

        self.console_clear_button = customtkinter.CTkButton(frame_option_buttons, text="❌ Clear Console",
                                                            command=clear_console)
        self.console_clear_button.grid(row=6, pady=10, padx=10)

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
                self.download_button.configure(state="disabled")
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
                title_file_safe = self.safe_filename(title)

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
                    file_path = os.path.join(download_path, title_file_safe + ".mp4")

                    if os.path.exists(file_path):
                        CTkMessagebox(title=f"{APPNAME} - Info", message=f"Info\n{title}.mp4 already exists.")
                        return
                    if win_sound == "True":
                        self.titel_label.configure(text=f"{title}")
                        video.download(download_path)
                        print(Fore.BLACK + Back.LIGHTBLUE_EX + f"Finished ✔️ -- Downloading / {title}")
                        self.progressbar_label.configure(text=f"Finished -- Downloading / {title}")
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    else:
                        self.titel_label.configure(text=f"{title}")
                        video.download(download_path)
                        print(Fore.BLACK + Back.LIGHTBLUE_EX + f"Finished ✔️ -- Downloading / {title}")
                        self.progressbar_label.configure(text=f"Finished -- Downloading / {title}")

                if self.mp3_mp4_combobox_var.get() == "MP3":
                    mp3_titel = title_file_safe + ".mp3"
                    audio = yt.streams.filter(only_audio=True).first()
                    download_path = os.path.join(os.getcwd(), DOWNLOAD_FOLDER)
                    file_path = os.path.join(download_path, mp3_titel)

                    if os.path.exists(file_path):
                        CTkMessagebox(title=f"{APPNAME} - Info", message=f"Info\n{title}.mp3 already exists.")
                        return
                    if win_sound == "True":
                        self.titel_label.configure(text=f"{title}")
                        audio.download(output_path=download_path, filename=mp3_titel)
                        self.progressbar_label.configure(text=f"Finished -- Downloading / {title}")
                        print(Fore.BLACK + Back.LIGHTBLUE_EX + f"Finished ✔️ -- Downloading / {title}")
                        winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
                    else:
                        self.titel_label.configure(text=f"{title}")
                        audio.download(output_path=download_path, filename=mp3_titel)
                        self.progressbar_label.configure(text=f"Finished -- Downloading / {title}")
                        print(Fore.BLACK + Back.LIGHTBLUE_EX + f"Finished ✔️ -- Downloading / {title}")


            except Exception as e:
                CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error:\n"
                                                                  f"{e}")
                print(Fore.BLACK + Back.LIGHTRED_EX + f"‼️ Error: {e}")
            finally:
                self.download_button.configure(state="normal")

        thread = threading.Thread(target=download)
        thread.start()

    def progressbar(self, stream, chunk, bytes_remaining):
        global prev_net_io
        net_io = psutil.net_io_counters()

        download_rate_kb = (net_io.bytes_recv - prev_net_io.bytes_recv) / 1024

        download_rate = download_rate_kb / 1024

        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        progress_decimal = bytes_downloaded / total_size

        progress = min(1, max(0, progress_decimal))

        self.progressbar_ctk.set(progress)

        self.progressbar_label.configure(
            text=f"{bytes_downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB -- {progress * 100:.2f}% complete  @ {download_rate:.2f} MB/s")
        print(Fore.BLACK + Back.LIGHTGREEN_EX +
              f"Downloading -- {bytes_downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB -- {progress * 100:.2f}% complete  @ {download_rate:.2f} MB/s")
        self.title(
            f"{APPNAME} -- Downloading - {progress * 100:.2f}% complete - {bytes_downloaded / (1024 * 1024):.2f} MB / {total_size / (1024 * 1024):.2f} MB  @ {download_rate:.2f} MB/s")
        prev_net_io = net_io

    def load_infos(self):
        def msg_box():
            CTkMessagebox(title=f"{APPNAME} - No valid URL", message=f"Pleas enter a valid URL.", icon="warning")

        url = self.url_entry.get()
        if url == "":
            msg_box()
        else:
            try:
                yt = YouTube(url)
                title = yt.title
                description = yt.description
                self.load_button.configure(state="disabled")
                print(Fore.BLACK + Back.LIGHTBLUE_EX + f"Loading: {title}")

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
                self.titel_label.configure(text=f"{title}")
            except Exception as e:
                CTkMessagebox(title=f"{APPNAME} - Error", message=f"Error:\n"
                                                                  f"{e}")
                print(Fore.BLACK + Back.LIGHTRED_EX + f"‼️ Error: {e}")
            finally:
                self.load_button.configure(state="normal")
                print(Fore.BLACK + Back.LIGHTGREEN_EX + f"Finished loading: {title}")

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
            print(Fore.BLACK + Back.LIGHTGREEN_EX + f"TXT safed as {filename}")
        except Exception as e:
            print(Fore.BLACK + Back.LIGHTRED_EX + f"‼️ Error: {e}")
            msg_box_error()

    def safe_filename(self, title):
        return pytube.helpers.safe_filename(title)

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
                print(Fore.BLACK + Back.LIGHTGREEN_EX + f"File saved as {filename}")
                msg_box_success()

        except Exception as e:
            print(Fore.BLACK + Back.LIGHTRED_EX + f"‼️ Error: {e}")

    def set_settings(self):
        json_data = get_json_data()
        for item in json_data:
            if item["id"] == 4:
                set_theme = item["content"]
                break
        pywinstyles.apply_style(PY_YT_DL, style=f"{set_theme}")

    def open_download_folder(self):
        downlaod_folder = os.path.join(os.getcwd(), DOWNLOAD_FOLDER)
        try:
            os.startfile(downlaod_folder)
        except Exception as e:
            CTkMessagebox(title=f"{APPNAME} - Error", message=f"Failed to open {downlaod_folder}\n"
                                                              f"{e}")
            print(Fore.BLACK + Back.LIGHTRED_EX + f"‼️ Error: {e}")


class Settings_Window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        self.title(f"{APPNAME} - Settings")
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

        self.allow_oauth_cache_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="OAUTH Cache:",
                                                              font=("bahnschrift", 15))
        self.allow_oauth_cache_label.grid(pady=20, padx=20, row=1, column=0)

        self.allow_oauth_cache_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame,
                                                                    values=["False", "True"], corner_radius=20)
        self.allow_oauth_cache_combobox.grid(pady=20, padx=20, row=1, column=1)

        self.win_sound_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="Win Sound",
                                                      font=("bahnschrift", 15))
        self.win_sound_label.grid(pady=20, padx=20, row=2, column=0)

        self.win_sound_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame, values=["False", "True"],
                                                            corner_radius=20)
        self.win_sound_combobox.grid(pady=20, padx=20, row=2, column=1)

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
