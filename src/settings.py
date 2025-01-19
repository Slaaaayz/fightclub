import json
import os

class Settings:
    def __init__(self):
        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0
        self.show_fps = False
        self.load_settings()

    def load_settings(self):
        try:
            with open("settings.json", 'r') as f:
                settings = json.load(f)
                self.master_volume = settings.get("master_volume", 1.0)
                self.music_volume = settings.get("music_volume", 1.0)
                self.sfx_volume = settings.get("sfx_volume", 1.0)
                self.show_fps = settings.get("show_fps", False)
        except:
            self.master_volume = 1.0
            self.music_volume = 1.0
            self.sfx_volume = 1.0
            self.show_fps = False

    def save_settings(self):
        settings = {
            "master_volume": self.master_volume,
            "music_volume": self.music_volume,
            "sfx_volume": self.sfx_volume,
            "show_fps": self.show_fps
        }
        try:
            with open("settings.json", 'w') as f:
                json.dump(settings, f)
                print(f"Settings saved - Show FPS: {'On' if self.show_fps else 'Off'}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}") 