import pygame
import pytmx
from src.player import Player
import random 
from src.menu import Menu

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Chargement de la map
        self.tmx_data = pytmx.load_pygame("Assets/maps/map.tmx")
        self.map_surface = self.create_map_surface()
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        
        # Création des joueurs aux points de spawn
        spawn_points = self.get_spawn_points()
        scaled_spawns = self.scale_positions(spawn_points)
        self.player1 = Player(scaled_spawns[0], "Assets/images/characters/Knight", 1)
        self.player2 = Player(scaled_spawns[1], "Assets/images/characters/Rogue", 2)

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
        
        # Ajouter la vérification des collisions d'attaque
        self.handle_player_collision()
        
        # Vérifier si un joueur a gagné
        if self.player1.lives <= 0 or self.player2.lives <= 0:
            winner = 2 if self.player1.lives <= 0 else 1
            action = self.show_game_over(winner)
            if action == "quit":
                self.running = False
                pygame.quit()
                exit()
            elif action == "replay":
                self.reset_game()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_surface, (0, 0))
        
        # Dessin des joueurs directement sur l'écran
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        
        # Affichage des barres de vie
        self.draw_health_bars()
        
        pygame.display.flip()

    def draw_health_bars(self):
        portrait_size = 50
        health_bar_width = 200
        health_bar_height = 20
        margin = 20
        
        # Utiliser le sprite actuel du SpriteManager au lieu de self.sprite
        player1_sprite = self.player1.sprite_manager.get_current_sprite()
        if player1_sprite:
            player_portrait = pygame.transform.scale(player1_sprite, (portrait_size, portrait_size))
        else:
            # Créer un portrait par défaut si pas de sprite
            player_portrait = pygame.Surface((portrait_size, portrait_size))
            player_portrait.fill((255, 0, 0))  # Rouge par défaut
        
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
        # Utiliser le sprite actuel du joueur 2
        player2_sprite = self.player2.sprite_manager.get_current_sprite()
        if player2_sprite:
            player2_portrait = pygame.transform.scale(player2_sprite, (portrait_size, portrait_size))
        else:
            player2_portrait = pygame.Surface((portrait_size, portrait_size))
            player2_portrait.fill((0, 0, 255))  # Bleu par défaut pour le joueur 2
        
        player2_portrait = pygame.transform.flip(player2_portrait, True, False)
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
        """Gère les collisions entre les joueurs et leurs attaques"""
        if self.player1.is_attacking and self.player1.attack_rect.colliderect(self.player2.rect):
            if not self.player2.invincible:  # Vérifier si le joueur 2 n'est pas invincible
                damage = self.player1.get_attack_damage()
                self.player2.take_damage(damage)
            
        if self.player2.is_attacking and self.player2.attack_rect.colliderect(self.player1.rect):
            if not self.player1.invincible:  # Vérifier si le joueur 1 n'est pas invincible
                damage = self.player2.get_attack_damage()
                self.player1.take_damage(damage)

    def reset_game(self):
        """Réinitialise le jeu sans recréer la fenêtre"""
        self.running = True
        spawn_points = self.get_spawn_points()
        scaled_spawns = self.scale_positions(spawn_points)
        self.player1 = Player(scaled_spawns[0], "Assets/images/characters/Knight", 1)
        self.player2 = Player(scaled_spawns[1], "Assets/images/characters/Rogue", 2)

    def show_game_over(self, winner):
        """Affiche l'écran de fin de partie"""
        # Jouer le son de mort
        self.player1.sound_manager.play_sound('death')
        
        # Configuration de base
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)  # Semi-transparent
        
        # Polices
        title_font = pygame.font.Font(None, 120)
        text_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        
        # Couleurs
        winner_colors = {
            1: (200, 50, 50),  # Rouge pour joueur 1
            2: (50, 50, 200)   # Bleu pour joueur 2
        }
        
        # Boutons
        button_width = 200
        button_height = 60
        button_margin = 20
        
        replay_button = pygame.Rect(self.width//2 - button_width - button_margin, 
                                  self.height * 3//4, 
                                  button_width, button_height)
        quit_button = pygame.Rect(self.width//2 + button_margin, 
                                self.height * 3//4, 
                                button_width, button_height)
        
        # Animation
        alpha = 0
        scale = 0.1
        rotation = 0
        
        clock = pygame.time.Clock()
        animation_done = False
        action = None
        
        while not animation_done:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.MOUSEBUTTONDOWN and scale > 0.8:  # Attendre que l'animation soit presque finie
                    if replay_button.collidepoint(event.pos):
                        action = "replay"
                        animation_done = True
                    elif quit_button.collidepoint(event.pos):
                        action = "quit"
                        animation_done = True
            
            # Mise à jour de l'animation
            if alpha < 200:
                alpha += 5
            if scale < 1:
                scale += 0.05
            rotation = (rotation + 2) % 360
            
            # Dessin
            self.screen.blit(self.map_surface, (0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Texte "GAME OVER"
            game_over_text = title_font.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.width//2, self.height//3))
            rotated_text = pygame.transform.rotozoom(game_over_text, rotation * (1-scale), scale)
            rotated_rect = rotated_text.get_rect(center=text_rect.center)
            self.screen.blit(rotated_text, rotated_rect)
            
            # Texte du gagnant
            if scale > 0.5:  # Apparaît après le "GAME OVER"
                winner_text = text_font.render(f"Player {winner} Wins!", True, winner_colors[winner])
                winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2))
                winner_text.set_alpha(alpha)
                self.screen.blit(winner_text, winner_rect)
                
                # Dessiner les boutons
                # Replay button
                button_color = (100, 255, 100) if replay_button.collidepoint(mouse_pos) else (50, 200, 50)
                pygame.draw.rect(self.screen, button_color, replay_button)
                replay_text = button_font.render("Replay", True, (255, 255, 255))
                self.screen.blit(replay_text, 
                               (replay_button.centerx - replay_text.get_width()//2,
                                replay_button.centery - replay_text.get_height()//2))
                
                # Quit button
                button_color = (255, 100, 100) if quit_button.collidepoint(mouse_pos) else (200, 50, 50)
                pygame.draw.rect(self.screen, button_color, quit_button)
                quit_text = button_font.render("Quit", True, (255, 255, 255))
                self.screen.blit(quit_text,
                               (quit_button.centerx - quit_text.get_width()//2,
                                quit_button.centery - quit_text.get_height()//2))
            
            pygame.display.flip()
            clock.tick(60)
        
        return action

    def run_menu(self):
        menu = Menu(self.screen)
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"
                
                result = menu.handle_event(event)
                if result is False:  # Le menu indique qu'il faut démarrer le jeu
                    self.reset_game()  # Réinitialiser le jeu avant de commencer
                    return "play"
            
            menu.draw()
            self.clock.tick(60)