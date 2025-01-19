import pygame
import pytmx
from src.player import Player
import random 
from src.menu import Menu
from src.sound_manager import SoundManager
from src.settings import Settings

class Game:
    def __init__(self, screen, resources):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Calculer le ratio d'aspect pour le scaling
        self.scale_x = self.width / 1280  # 1280 est la résolution de base
        self.scale_y = self.height / 720  # 720 est la résolution de base
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.resources = resources
        self.sound_manager = resources.sound_manager
        self.settings = resources.settings
        
        # Chargement de la map
        self.tmx_data = pytmx.load_pygame("Assets/maps/map.tmx")
        self.map_surface = self.create_map_surface()
        self.map_surface = pygame.transform.scale(self.map_surface, (self.width, self.height))
        
        # Création des joueurs
        spawn_points = self.get_spawn_points()
        scaled_spawns = self.scale_positions(spawn_points)
        self.player1 = Player(scaled_spawns[0], "Assets/images/characters/Knight", 1)
        self.player2 = Player(scaled_spawns[1], "Assets/images/characters/Rogue", 2)
        
        # Assigner le sound_manager aux joueurs
        self.player1.sound_manager = self.sound_manager
        self.player2.sound_manager = self.sound_manager

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
                spawn_num = int(obj.name[-1]) 
                spawn_y = obj.y - 100  
                spawn_dict[spawn_num] = (obj.x, spawn_y)
        
        # Sélectionner aléatoirement 2 points de spawn différents
        if len(spawn_dict) >= 2:
            spawn_numbers = random.sample(list(spawn_dict.keys()), 2)
            spawn_points = [spawn_dict[num] for num in spawn_numbers]
        else:
            # Points de spawn par défaut si pas assez de points définis
            spawn_points = [
                (self.width * 0.25, self.height * 0.3),  
                (self.width * 0.75, self.height * 0.3)
            ]
        
        return spawn_points

    def scale_positions(self, positions):
        # Mise à jour de la méthode pour utiliser les ratios d'aspect
        original_width = self.tmx_data.width * self.tmx_data.tilewidth
        original_height = self.tmx_data.height * self.tmx_data.tileheight
        
        scaled_positions = []
        for pos in positions:
            scaled_x = pos[0] * self.scale_x
            scaled_y = pos[1] * self.scale_y
            scaled_positions.append((scaled_x, scaled_y))
        return scaled_positions

    def get_obstacles(self):
        obstacles = []
        
        for obj in self.tmx_data.objects:
            if obj.type == "obstacle":
                scaled_rect = pygame.Rect(
                    obj.x * self.scale_x,
                    obj.y * self.scale_y,
                    obj.width * self.scale_x,
                    obj.height * self.scale_y
                )
                obstacles.append(scaled_rect)
        return obstacles

    def run(self):
        self.settings.load_settings()
        self.apply_settings()
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    action = self.show_pause_menu()
                    if action == "menu":
                        self.running = False
                        return "menu"

    def update(self):
        self.player1.update(self.get_obstacles())
        self.player2.update(self.get_obstacles())
        
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
            elif action == "menu":
                self.running = False
                return "menu"

        # Mettre à jour les volumes
        self.sound_manager.set_master_volume(self.settings.master_volume)
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sfx_volume)

    def draw_fps(self):
        if self.settings.show_fps:
            fps = str(int(self.clock.get_fps()))
            fps_surface = pygame.font.Font(None, 36).render(fps, True, (255, 255, 255))
            fps_rect = fps_surface.get_rect(bottomright=(self.width - 10, self.height - 10))
            self.screen.blit(fps_surface, fps_rect)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.map_surface, (0, 0))
        
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)
        self.draw_health_bars()
        self.draw_fps()
        
        pygame.display.flip()

    def draw_health_bars(self):
        portrait_size = 50
        health_bar_width = 200
        health_bar_height = 20
        margin = 20
        
        player1_sprite = self.player1.sprite_manager.get_current_sprite()
        if player1_sprite:
            player_portrait = pygame.transform.scale(player1_sprite, (portrait_size, portrait_size))
        else:
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
        if self.player1.is_attacking and self.player1.attack_rect.colliderect(self.player2.rect):
            if not self.player2.invincible:  # Vérifier si le joueur 2 n'est pas invincible
                damage = self.player1.get_attack_damage()
                self.player2.take_damage(damage)
            
        if self.player2.is_attacking and self.player2.attack_rect.colliderect(self.player1.rect):
            if not self.player1.invincible:  # Vérifier si le joueur 1 n'est pas invincible
                damage = self.player2.get_attack_damage()
                self.player1.take_damage(damage)

    def reset_game(self):
        self.settings.load_settings()
        self.apply_settings()
        
        self.running = True
        spawn_points = self.get_spawn_points()
        scaled_spawns = self.scale_positions(spawn_points)
        self.player1 = Player(scaled_spawns[0], "Assets/images/characters/Knight", 1)
        self.player2 = Player(scaled_spawns[1], "Assets/images/characters/Rogue", 2)
        
        self.player1.sound_manager = self.sound_manager
        self.player2.sound_manager = self.sound_manager

    def show_game_over(self, winner):
        self.settings.load_settings()
        self.apply_settings()
        
        self.sound_manager.play_sound('death')
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(200)  
        title_font = pygame.font.Font(None, 120)
        text_font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        
        winner_colors = {
            1: (200, 50, 50),  # Rouge pour joueur 1
            2: (50, 50, 200)   # Bleu pour joueur 2
        }
        
        button_width = 200
        button_height = 60
        button_margin = 20
        
        replay_button = pygame.Rect(self.width//2 - button_width - button_margin, 
                                  self.height * 3//4, 
                                  button_width, button_height)
        menu_button = pygame.Rect(self.width//2 + button_margin, 
                                self.height * 3//4, 
                                button_width, button_height)
        
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
                if event.type == pygame.MOUSEBUTTONDOWN and scale > 0.8:
                    if replay_button.collidepoint(event.pos):
                        action = "replay"
                        animation_done = True
                    elif menu_button.collidepoint(event.pos):  
                        action = "menu" 
                        animation_done = True
            
            if alpha < 200:
                alpha += 5
            if scale < 1:
                scale += 0.05
            rotation = (rotation + 2) % 360
            
            self.screen.blit(self.map_surface, (0, 0))
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = title_font.render("GAME OVER", True, (255, 255, 255))
            text_rect = game_over_text.get_rect(center=(self.width//2, self.height//3))
            rotated_text = pygame.transform.rotozoom(game_over_text, rotation * (1-scale), scale)
            rotated_rect = rotated_text.get_rect(center=text_rect.center)
            self.screen.blit(rotated_text, rotated_rect)
            
            if scale > 0.5:
                winner_text = text_font.render(f"Player {winner} Wins!", True, winner_colors[winner])
                winner_rect = winner_text.get_rect(center=(self.width//2, self.height//2))
                winner_text.set_alpha(alpha)
                self.screen.blit(winner_text, winner_rect)
                
              
                button_color = (100, 255, 100) if replay_button.collidepoint(mouse_pos) else (50, 200, 50)
                pygame.draw.rect(self.screen, button_color, replay_button)
                replay_text = button_font.render("Replay", True, (255, 255, 255))
                self.screen.blit(replay_text, 
                               (replay_button.centerx - replay_text.get_width()//2,
                                replay_button.centery - replay_text.get_height()//2))
                
                button_color = (255, 100, 100) if menu_button.collidepoint(mouse_pos) else (200, 50, 50)
                pygame.draw.rect(self.screen, button_color, menu_button)
                menu_text = button_font.render("Menu", True, (255, 255, 255))
                self.screen.blit(menu_text,
                               (menu_button.centerx - menu_text.get_width()//2,
                                menu_button.centery - menu_text.get_height()//2))
            
            self.draw_fps()
            
            pygame.display.flip()
            clock.tick(60)
        
        return action

    def run_menu(self):
        menu = Menu(self.screen, self.resources, is_temp_menu=False)
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "quit"
                
                result = menu.handle_event(event)
                if result is False:  
                    self.reset_game() 
                    return "play"
            
            menu.draw()
            self.draw_fps()
            pygame.display.flip()
            self.clock.tick(60)

    def show_pause_menu(self):
        self.settings.load_settings()
        self.sound_manager.set_master_volume(self.settings.master_volume)
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sfx_volume)
        
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        
        font = pygame.font.Font(None, 74)
        button_font = pygame.font.Font(None, 50)
        COLOR_INACTIVE = (40, 40, 60)
        COLOR_HOVER = (60, 60, 80)
        COLOR_TEXT = (255, 255, 255)
        
        pause_text = font.render("PAUSE", True, COLOR_TEXT)
        pause_rect = pause_text.get_rect(center=(self.width/2, self.height * 0.3))
        
        button_width = 200
        button_height = 50
        button_margin = 20
        
        resume_button = pygame.Rect(self.width/2 - button_width/2,
                                  self.height * 0.45,
                                  button_width, button_height)
        
        menu_button = pygame.Rect(self.width/2 - button_width/2,
                                 self.height * 0.45 + button_height + button_margin,
                                 button_width, button_height)
        
        quit_button = pygame.Rect(self.width/2 - button_width/2,
                                 self.height * 0.45 + (button_height + button_margin) * 2,
                                 button_width, button_height)
        
        paused = True
        in_settings = False
        settings_menu = None
        last_hover = None 
        
        while paused:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if in_settings:
                            in_settings = False
                        else:
                            paused = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if in_settings:
                        if settings_menu:
                            if settings_menu.handle_event(event) == "back":
                                in_settings = False
                    else:
                        if resume_button.collidepoint(mouse_pos):
                            paused = False
                        elif menu_button.collidepoint(mouse_pos):
                            return "menu"
                        elif quit_button.collidepoint(mouse_pos):
                            self.sound_manager.stop_background_music()
                            self.running = False
                            pygame.quit()
                            exit()
            
            if in_settings and settings_menu:
                settings_menu.handle_event(event)
        
            self.screen.blit(self.map_surface, (0, 0))
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.draw_health_bars()
            
            self.screen.blit(overlay, (0, 0))
            
            if in_settings and settings_menu:
                settings_menu.draw()
            else:
                self.screen.blit(pause_text, pause_rect)
                
                if paused and not in_settings:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    resume_button = pygame.Rect(self.width/2 - 100, self.height/2 - 100, 200, 50)
                    menu_button = pygame.Rect(self.width/2 - 100, self.height/2, 200, 50)
                    quit_button = pygame.Rect(self.width/2 - 100, self.height/2 + 100, 200, 50)
                    
                    current_hover = None
                    if resume_button.collidepoint(mouse_pos):
                        current_hover = "resume"
                    elif menu_button.collidepoint(mouse_pos):
                        current_hover = "menu"
                    elif quit_button.collidepoint(mouse_pos):
                        current_hover = "quit"
                    
                    if current_hover != last_hover and current_hover is not None:
                        self.sound_manager.play_sound('hover', volume=0.3)
                    last_hover = current_hover
                    
                    COLOR_INACTIVE = (40, 40, 60)
                    COLOR_HOVER = (60, 60, 80)
                    
                    pygame.draw.rect(self.screen, 
                        COLOR_HOVER if resume_button.collidepoint(mouse_pos) else COLOR_INACTIVE, 
                        resume_button)
                    pygame.draw.rect(self.screen, 
                        COLOR_HOVER if menu_button.collidepoint(mouse_pos) else COLOR_INACTIVE, 
                        menu_button)
                    pygame.draw.rect(self.screen, 
                        COLOR_HOVER if quit_button.collidepoint(mouse_pos) else COLOR_INACTIVE, 
                        quit_button)
                    
                    default_font = pygame.font.Font(None, 50)
                    resume_text = default_font.render("Resume", True, (255, 255, 255))
                    menu_text = default_font.render("Menu", True, (255, 255, 255))
                    quit_text = default_font.render("Quit", True, (255, 255, 255))
                    
                    self.screen.blit(resume_text, resume_text.get_rect(center=resume_button.center))
                    self.screen.blit(menu_text, menu_text.get_rect(center=menu_button.center))
                    self.screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
            
            self.draw_fps()
            
            pygame.display.flip()
            self.clock.tick(60)

    def apply_settings(self):
        self.sound_manager.set_master_volume(self.settings.master_volume)
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sfx_volume)