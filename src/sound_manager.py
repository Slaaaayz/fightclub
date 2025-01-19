import pygame
import os

class SoundManager:
    def __init__(self):
        # Initialiser le mixer de pygame
        pygame.mixer.init()
        
        # Dictionnaire pour stocker les sons
        self.sounds = {}
        
        # Volume par défaut
        self.volume = 0.5  # 50% du volume
        
        # Charger les sons
        self.load_sounds()
        
    def load_sounds(self):
        """Charge tous les effets sonores"""
        sound_files = {
            'jump': 'jump.mp3',
            'hit': 'hit.mp3',
            'death': 'death.mp3',
            'attack': 'attack.mp3',
            'hurt': 'hurt.mp3'
        }
        
        # Chemin vers le dossier des sons
        sounds_path = "Assets/sounds"
        
        # Charger chaque son
        for sound_name, file_name in sound_files.items():
            try:
                sound_path = os.path.join(sounds_path, file_name)
                if os.path.exists(sound_path):
                    try:
                        sound = pygame.mixer.Sound(sound_path)
                    except pygame.error:
                        # Si le chargement direct échoue, essayer avec music.load()
                        pygame.mixer.music.load(sound_path)
                        pygame.mixer.music.set_volume(self.volume)
                        # Créer un objet Sound factice qui utilisera music
                        sound = type('Sound', (), {
                            'play': lambda: pygame.mixer.music.play(),
                            'set_volume': lambda v: pygame.mixer.music.set_volume(v)
                        })()
                    
                    sound.set_volume(self.volume)
                    self.sounds[sound_name] = sound
                    print(f"Son chargé: {sound_path}")
                else:
                    print(f"Fichier son non trouvé: {sound_path}")
            except Exception as e:
                print(f"Erreur lors du chargement du son {file_name}: {e}")
    
    def play_sound(self, sound_name):
        """Joue un son spécifique"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Erreur lors de la lecture du son {sound_name}: {e}")
    
    def set_volume(self, volume):
        """Définit le volume global des effets sonores (0.0 à 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume) 