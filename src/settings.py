import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "show_fps": True,
            "master_volume": 1.0,
            "music_volume": 0.25,
            "sfx_volume": 0.7
        }
        self.load_settings()

    def load_settings(self):
        """Charge les paramètres depuis le fichier settings.json"""
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)
                self.show_fps = settings.get("show_fps", self.default_settings["show_fps"])
                self.master_volume = settings.get("master_volume", self.default_settings["master_volume"])
                self.music_volume = settings.get("music_volume", self.default_settings["music_volume"])
                self.sfx_volume = settings.get("sfx_volume", self.default_settings["sfx_volume"])
        except:
            self.__dict__.update(self.default_settings)

    def save_settings(self):
        """Sauvegarde les paramètres dans le fichier settings.json"""
        settings = {
            "show_fps": self.show_fps,
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
                print(f"Settings saved - Show FPS: {self.show_fps}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}") 