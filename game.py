import pygame
import pytmx
from player import Player
from camera import Camera
import random 

class Game:
    def __init__(self):
        pygame.init()
        # Initialisation en plein écran
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Chargement de la map
        self.tmx_data = pytmx.load_pygame("map.tmx")
        self.map_surface = self.create_map_surface()
        # Redimensionner la surface de la map pour qu'elle s'adapte à l'écran
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        
        # Création des joueurs aux points de spawn
        spawn_points = self.get_spawn_points()
        # Ajuster les positions de spawn en fonction de la nouvelle taille
        scaled_spawns = self.scale_positions(spawn_points)
        self.player1 = Player(scaled_spawns[0], "player.png", 1)
        self.player2 = Player(scaled_spawns[1], "player.png", 2)
        
        # Création de la caméra
        self.camera = Camera(self.width, self.height)

    def create_map_surface(self):
        # Création de la surface de la map
        temp_surface = pygame.Surface((
            self.tmx_data.width * self.tmx_data.tilewidth,
            self.tmx_data.height * self.tmx_data.tileheight
        ))
        
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        temp_surface.blit(tile, (x * self.tmx_data.tilewidth, 
                                               y * self.tmx_data.tileheight))
        return temp_surface

    def get_spawn_points(self):
        spawn_points = []
        spawn_dict = {}  
        
        # Récupérer tous les points de spawn
        for obj in self.tmx_data.objects:
            if obj.type == "Spawn":
                spawn_num = int(obj.name[-1])  # Prend le dernier caractère du nom
                spawn_y = obj.y - 100  # Augmenté à -100 pour un spawn plus haut car ça bug pour l'instant
                spawn_dict[spawn_num] = (obj.x, spawn_y)
        
        # Sélectionner aléatoirement 2 points de spawn différents
        if len(spawn_dict) >= 2:
            spawn_numbers = random.sample(list(spawn_dict.keys()), 2)
            spawn_points = [spawn_dict[num] for num in spawn_numbers]
        else:
            # Points de spawn par défaut si pas assez de points définis
            spawn_points = [
                (self.width * 0.25, self.height * 0.3),  # Spawn plus haut par défaut
                (self.width * 0.75, self.height * 0.3)
            ]
        
        return spawn_points

    def scale_positions(self, positions):
        original_width = self.tmx_data.width * self.tmx_data.tilewidth
        original_height = self.tmx_data.height * self.tmx_data.tileheight
        scale_x = self.width / original_width
        scale_y = self.height / original_height
        
        scaled_positions = []
        for pos in positions:
            scaled_positions.append((pos[0] * scale_x, pos[1] * scale_y))
        return scaled_positions

    def get_obstacles(self):
        obstacles = []
        scale_x = self.width / (self.tmx_data.width * self.tmx_data.tilewidth)
        scale_y = self.height / (self.tmx_data.height * self.tmx_data.tileheight)
        
        for obj in self.tmx_data.objects:
            if obj.type == "obstacle":
                scaled_rect = pygame.Rect(
                    obj.x * scale_x,
                    obj.y * scale_y,
                    obj.width * scale_x,
                    obj.height * scale_y
                )
                obstacles.append(scaled_rect)
        return obstacles

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        self.player1.update(self.get_obstacles())
        self.player2.update(self.get_obstacles())
        
        # Vérifier si un joueur a gagné
        if self.player1.lives <= 0 or self.player2.lives <= 0:
            self.running = False  # Fin du jeu
        
        self.camera.update(self.player1, self.player2)
        
        # Gestion des collisions entre joueurs
        if self.player1.rect.colliderect(self.player2.rect):
            self.handle_player_collision()

    def draw(self):
        self.screen.fill((0, 0, 0))
        
        self.screen.blit(self.map_surface, (0, 0))
        
        self.player1.draw(self.screen, self.camera)
        self.player2.draw(self.screen, self.camera)
        
        # Affichage des barres de vie
        self.draw_health_bars()
        
        pygame.display.flip()

    def draw_health_bars(self):
        portrait_size = 50
        health_bar_width = 200
        health_bar_height = 20
        margin = 20
        
        player_portrait = pygame.transform.scale(self.player1.sprite, (portrait_size, portrait_size))
        
        # Interface du joueur 1 (gauche)
        self.screen.blit(player_portrait, (margin, margin))
        # Contour de la barre de vie
        pygame.draw.rect(self.screen, (100, 100, 100), 
                        (margin + portrait_size + 10, margin + portrait_size//2 - health_bar_height//2,
                         health_bar_width, health_bar_height))
        # Barre de vie
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (margin + portrait_size + 10, margin + portrait_size//2 - health_bar_height//2,
                         health_bar_width * (self.player1.health/100), health_bar_height))
        
        # Interface du joueur 2 (droite)
        player2_portrait = pygame.transform.flip(player_portrait, True, False)
        portrait_x = self.width - margin - portrait_size
        self.screen.blit(player2_portrait, (portrait_x, margin))
        # Contour de la barre de vie
        pygame.draw.rect(self.screen, (100, 100, 100),
                        (portrait_x - health_bar_width - 10, margin + portrait_size//2 - health_bar_height//2,
                         health_bar_width, health_bar_height))
        # Barre de vie
        pygame.draw.rect(self.screen, (255, 0, 0),
                        (portrait_x - health_bar_width - 10, margin + portrait_size//2 - health_bar_height//2,
                         health_bar_width * (self.player2.health/100), health_bar_height))
        
        # Affichage des vies et pourcentages
        font = pygame.font.Font(None, 36)
        # Joueur 1
        lives_text = font.render(f"×{self.player1.lives}", True, (255, 255, 255))
        health_text = font.render(f"{int(self.player1.health)}%", True, (255, 255, 255))
        self.screen.blit(lives_text, (margin + portrait_size + 10, margin))
        self.screen.blit(health_text, (margin + portrait_size + health_bar_width//2 - health_text.get_width()//2,
                                     margin + portrait_size + 5))
        
        # Joueur 2
        lives_text = font.render(f"×{self.player2.lives}", True, (255, 255, 255))
        health_text = font.render(f"{int(self.player2.health)}%", True, (255, 255, 255))
        self.screen.blit(lives_text, (portrait_x - 40, margin))
        self.screen.blit(health_text, (portrait_x - health_bar_width//2 - health_text.get_width()//2,
                                     margin + portrait_size + 5))

    def handle_player_collision(self):
        if self.player1.is_attacking and self.player1.attack_rect.colliderect(self.player2.rect):
            damage = self.player1.get_attack_damage()
            self.player2.take_damage(damage)
            
        if self.player2.is_attacking and self.player2.attack_rect.colliderect(self.player1.rect):
            damage = self.player2.get_attack_damage()
            self.player1.take_damage(damage) 