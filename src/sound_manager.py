import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        
        # Volumes par défaut
        self.master_volume = 0.5
        self.music_volume = 0.5
        self.sfx_volume = 0.5
        
        # Charger les sons
        self.load_sounds()
        self.load_background_music()
    
    def load_sounds(self):
        sound_files = {
            'jump': 'jump.mp3',
            'hit': 'hit.mp3',
            'death': 'death.mp3',
            'attack': 'attack.mp3',
            'hurt': 'hurt.mp3',
            'hover': 'hover.mp3'
        }
        
        for name, file in sound_files.items():
            try:
                sound_path = os.path.join("Assets/sounds", file)
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    sound.set_volume(self.master_volume * self.sfx_volume)
                    self.sounds[name] = sound
            except Exception as e:
                print(f"Erreur chargement son {file}: {e}")
    
    def load_background_music(self):
        try:
            music_path = os.path.join("Assets/music", "background.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
        except Exception as e:
            print(f"Erreur chargement musique: {e}")
    
    def play_sound(self, name, volume=None):
        if name in self.sounds:
            try:
                if volume is not None:
                    current_volume = self.sounds[name].get_volume()
                    temp_volume = volume * self.master_volume * self.sfx_volume
                    self.sounds[name].set_volume(temp_volume)
                    self.sounds[name].play()
                    self.sounds[name].set_volume(current_volume)
                else:
                    self.sounds[name].play()
            except Exception as e:
                print(f"Erreur lors de la lecture du son {name}: {e}")
    
    def play_background_music(self):
        try:
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(-1)  
                pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
        except Exception as e:
            print(f"Erreur lors de la lecture de la musique: {e}")
    
    def stop_background_music(self):
        pygame.mixer.music.stop()
    
    def set_master_volume(self, volume):
        self.master_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume * self.sfx_volume)
    
    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
    
    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume * self.sfx_volume) 