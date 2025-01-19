import pygame
import os

class SpriteManager:
    def __init__(self):
        self.sprites = {}
        self.current_animation = None
        self.current_frame = 0
        self.frame_counter = 0
        
        # Nombre de frames de jeu à attendre avant de changer de frame d'animation
        self.animation_speeds = {
            'idle': 8,      
            'run': 8,       
            'jump': 8,      
            'attack1': 4,   
            'attack2': 4,   
            'attack3': 4,   
            'hit': 8,       
            'death': 10     
        }
        
        # Ajouter le nombre de frames pour chaque animation
        self.animation_lengths = {
            'attack1': 4,  # Exemple: l'animation d'attaque légère a 4 frames
            'attack2': 4,  # Attaque lourde
            'attack3': 4,  # Attaque spéciale
        }
        
        self.is_flipped = False
        self.animation_finished = False

    def load_sprite_sheets(self, character_path):
        """Charge toutes les feuilles de sprites pour les différentes animations"""
        # Mapping des noms de dossiers vers les noms d'animations
        animation_folders = {
            'Idle': 'idle',
            'Attack': 'attack1',
            'Run_Attack': 'attack2',
            'Attack_Extra': 'attack3',
            'Run': 'run',
            'Jump': 'jump',
            'Fall': 'fall',
            'Death': 'death',
            'Hurt': 'hit'
        }
        
        animations = {
            'idle': [],
            'run': [],
            'jump': [],
            'fall': [],
            'attack1': [],
            'attack2': [],
            'attack3': [],
            'hit': [],
            'death': []
        }

        # Créer un sprite par défaut au cas où aucun n'est trouvé
        default_surface = pygame.Surface((50, 50))
        default_surface.fill((255, 0, 0))  # Rouge par défaut
        
        sprites_loaded = False
        
        # Parcourir les dossiers d'animations
        for folder_name, anim_name in animation_folders.items():
            folder_path = os.path.join(character_path, folder_name)
            if os.path.exists(folder_path):
                # Chercher tous les fichiers PNG numérotés
                frame_files = sorted([f for f in os.listdir(folder_path) 
                                    if f.lower().endswith('.png')],
                                   key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))
                
                if frame_files:
                    for frame_file in frame_files:
                        frame_path = os.path.join(folder_path, frame_file)
                        try:
                            sprite = pygame.image.load(frame_path).convert_alpha()
                            animations[anim_name].append(sprite)
                            sprites_loaded = True
                            print(f"Chargé: {frame_path}")  # Debug
                        except (pygame.error, FileNotFoundError) as e:
                            print(f"Erreur lors du chargement de {frame_path}: {e}")
        
        # Si aucun sprite n'a été chargé, utiliser le sprite par défaut
        if not sprites_loaded:
            print(f"Attention: Aucun sprite trouvé dans {character_path}. Utilisation du sprite par défaut.")
            for animation_name in animations.keys():
                animations[animation_name].append(default_surface)
        else:
            print(f"Sprites chargés avec succès pour {character_path}")
        
        self.sprites = animations
        self.current_animation = 'idle'

    def get_current_sprite(self):
        """Retourne le sprite actuel de l'animation en cours"""
        if not self.sprites or self.current_animation not in self.sprites:
            return None
            
        animation_frames = self.sprites[self.current_animation]
        if not animation_frames:
            return None

        sprite = animation_frames[self.current_frame]
        if self.is_flipped:
            sprite = pygame.transform.flip(sprite, True, False)
        return sprite

    def update(self, dt):
        if self.current_animation is None:
            return
            
        self.frame_counter += 1
        animation_speed = self.animation_speeds.get(self.current_animation, 8)
        
        if self.frame_counter >= animation_speed:
            self.frame_counter = 0
            
            # Pour les animations d'attaque
            if self.current_animation in self.animation_lengths:
                # Ne pas incrémenter si on a déjà atteint la dernière frame
                if self.current_frame < self.animation_lengths[self.current_animation] - 1:
                    self.current_frame += 1
                else:
                    self.animation_finished = True
                    self.current_animation = 'idle'
                    self.current_frame = 0
            else:
                # Pour les animations en boucle (idle, run, jump)
                self.current_frame = (self.current_frame + 1) % len(self.sprites[self.current_animation])

    def set_animation(self, animation_name, force=False):
        """Change l'animation en cours"""
        if animation_name not in self.sprites:
            return False
            
        # Ne pas démarrer une nouvelle animation d'attaque si une est déjà en cours
        if self.current_animation in self.animation_lengths and not self.animation_finished:
            if animation_name in self.animation_lengths and not force:
                return False
        
        if self.current_animation != animation_name or force:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_counter = 0
            self.animation_finished = False
        return True

    def set_flip(self, flip):
        """Définit si le sprite doit être retourné horizontalement"""
        self.is_flipped = flip 