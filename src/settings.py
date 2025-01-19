import json
import os

class Settings:
    def __init__(self):
        self.fullscreen = True
        self.show_fps = False
        self.master_volume = 0.7
        self.music_volume = 0.7
        self.sfx_volume = 0.7
        self.settings_file = "settings.json"
        self.load_settings()

    def load_settings(self):
        """Charge les paramètres depuis le fichier settings.json"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    data = json.load(f)
                    self.fullscreen = data.get('fullscreen', True)
                    self.show_fps = data.get('show_fps', False)
                    self.master_volume = data.get('master_volume', 0.7)
                    self.music_volume = data.get('music_volume', 0.7)
                    self.sfx_volume = data.get('sfx_volume', 0.7)
                    print(f"Settings loaded - Show FPS: {self.show_fps}")
            except Exception as e:
                print(f"Erreur lors du chargement des paramètres: {e}")

    def save_settings(self):
        """Sauvegarde les paramètres dans le fichier settings.json"""
        data = {
            'fullscreen': self.fullscreen,
            'show_fps': self.show_fps,
            'master_volume': self.master_volume,
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(data, f)
            print(f"Settings saved - Show FPS: {self.show_fps}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}") 