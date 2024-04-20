import customtkinter
from variables import APPNAME


class Settings_Window(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f"{APPNAME} - Settings")

        self.settings_label = customtkinter.CTkLabel(self, text="Settings", font=("bahnschrift", 30))
        self.settings_label.grid(row=0, column=0, pady=20, padx=20, columnspan=3)

        self.video_settings = customtkinter.CTkLabel(self, text="Video", font=("bahnschrift", 20))
        self.video_settings.grid(row=1, column=0, pady=20, padx=20)

        self.audio_settings = customtkinter.CTkLabel(self, text="Audio", font=("bahnschrift", 20))
        self.audio_settings.grid(row=1, column=1, pady=20, padx=20)

        self.miscellaneous_settings = customtkinter.CTkLabel(self, text="Miscellaneous", font=("bahnschrift", 20))
        self.miscellaneous_settings.grid(row=1, column=2, pady=20, padx=20)

        self.frame_video_settings = customtkinter.CTkFrame(self, width=500, height=400, corner_radius=40)
        self.frame_video_settings.grid(pady=20, padx=20, sticky="n", row=3, column=0)

        self.frame_audio_settings = customtkinter.CTkFrame(self, width=500, height=400, corner_radius=40)
        self.frame_audio_settings.grid(pady=20, padx=20, sticky="n", row=3, column=1)

        self.miscellaneous_settings_frame = customtkinter.CTkFrame(self, width=500, height=400, corner_radius=40)
        self.miscellaneous_settings_frame.grid(pady=20, padx=20, sticky="n", row=3, column=2)

        self.video_resolution_label = customtkinter.CTkLabel(self.frame_video_settings, text="Resolution:",
                                                             font=("bahnschrift", 15))
        self.video_resolution_label.grid(pady=20, padx=20, row=0, column=0)

        self.video_resolution_combobox = customtkinter.CTkComboBox(self.frame_video_settings)
        self.video_resolution_combobox.grid(pady=20, padx=20, row=0, column=1)

        self.video_filetype_label = customtkinter.CTkLabel(self.frame_video_settings, text="Filetype:",
                                                           font=("bahnschrift", 15))
        self.video_filetype_label.grid(pady=20, padx=20, row=1, column=0)

        self.video_filetype_combobox = customtkinter.CTkComboBox(self.frame_video_settings)
        self.video_filetype_combobox.grid(pady=20, padx=20, row=1, column=1)

        self.video_fps_label = customtkinter.CTkLabel(self.frame_video_settings, text="FPS:", font=("bahnschrift", 15))
        self.video_fps_label.grid(pady=20, padx=20, row=2, column=0)

        self.video_fps_combobox = customtkinter.CTkComboBox(self.frame_video_settings)
        self.video_fps_combobox.grid(pady=20, padx=20, row=2, column=1)

        self.video_codec_label = customtkinter.CTkLabel(self.frame_video_settings, text="Video Codec:",
                                                        font=("bahnschrift", 15))
        self.video_codec_label.grid(pady=20, padx=20, row=3, column=0)

        self.video_codec_combobox = customtkinter.CTkComboBox(self.frame_video_settings)
        self.video_codec_combobox.grid(pady=20, padx=20, row=3, column=1)

        self.video_bitrate_label = customtkinter.CTkLabel(self.frame_video_settings, text="Bitrate:",
                                                          font=("bahnschrift", 15))
        self.video_bitrate_label.grid(pady=20, padx=20, row=4, column=0)

        self.video_bitrate_combobox = customtkinter.CTkComboBox(self.frame_video_settings)
        self.video_bitrate_combobox.grid(pady=20, padx=20, row=4, column=1)

        self.audio_filetype_label = customtkinter.CTkLabel(self.frame_audio_settings, text="Filetype:",
                                                           font=("bahnschrift", 15))
        self.audio_filetype_label.grid(pady=20, padx=20, row=0, column=0)

        self.audio_filetype_combobox = customtkinter.CTkComboBox(self.frame_audio_settings)
        self.audio_filetype_combobox.grid(pady=20, padx=20, row=0, column=1)

        self.audio_codec_label = customtkinter.CTkLabel(self.frame_audio_settings, text="Codec:",
                                                        font=("bahnschrift", 15))
        self.audio_codec_label.grid(pady=20, padx=20, row=1, column=0)

        self.audio_codec_combobox = customtkinter.CTkComboBox(self.frame_audio_settings)
        self.audio_codec_combobox.grid(pady=20, padx=20, row=1, column=1)

        self.audio_bitrate_label = customtkinter.CTkLabel(self.frame_audio_settings, text="Bitrate:",
                                                          font=("bahnschrift", 15))
        self.audio_bitrate_label.grid(pady=20, padx=20, row=2, column=0)

        self.audio_bitrate_combobox = customtkinter.CTkComboBox(self.frame_audio_settings)
        self.audio_bitrate_combobox.grid(pady=20, padx=20, row=2, column=1)

        self.miscellaneous_use_oauth_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="OAUTH:",
                                                                    font=("bahnschrift", 15))
        self.miscellaneous_use_oauth_label.grid(pady=20, padx=20, row=0, column=0)

        self.miscellaneous_use_oauth_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame)
        self.miscellaneous_use_oauth_combobox.grid(pady=20, padx=20, row=0, column=1)

        self.allow_oauth_cache_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="OAUTH Cache:",
                                                              font=("bahnschrift", 15))
        self.allow_oauth_cache_label.grid(pady=20, padx=20, row=1, column=0)

        self.allow_oauth_cache_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame)
        self.allow_oauth_cache_combobox.grid(pady=20, padx=20, row=1, column=1)

        self.win_sound_label = customtkinter.CTkLabel(self.miscellaneous_settings_frame, text="Win Sound",
                                                      font=("bahnschrift", 15))
        self.win_sound_label.grid(pady=20, padx=20, row=2, column=0)

        self.win_sound_combobox = customtkinter.CTkComboBox(self.miscellaneous_settings_frame)
        self.win_sound_combobox.grid(pady=20, padx=20, row=2, column=1)
