import pygame
import math
from src.sprite_manager import SpriteManager
from src.sound_manager import SoundManager

class Player:
    def __init__(self, pos, sprite_path, player_num):
        # Initialisation du sprite manager
        self.sprite_manager = SpriteManager()
        try:
            self.sprite_manager.load_sprite_sheets(sprite_path)
        except Exception as e:
            print(f"Erreur lors du chargement des sprites pour le joueur {player_num}: {e}")
        
        # Obtenir le premier sprite pour initialiser le rect
        initial_sprite = self.sprite_manager.get_current_sprite()
        if initial_sprite:
            self.rect = initial_sprite.get_rect()
        else:
            print(f"Attention: Utilisation d'un rectangle par défaut pour le joueur {player_num}")
            self.rect = pygame.Rect(0, 0, 50, 50)
        
        self.rect.x, self.rect.y = pos
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.5)  # Activer la gravité immédiatement
        self.speed = 5
        self.jump_power = -12
        self.can_double_jump = True
        self.is_spawning = False  # Désactiver l'état de spawn
        
        self.health = 100
        self.lives = 3  # Nombre de vies initial
        self.respawn_pos = pos  # Sauvegarder la position de spawn
        self.is_dead = False  # État de mort temporaire
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None  # Pour différents types d'attaques
        self.attack_rect = pygame.Rect(0, 0, 50, 50)
        self.attack_direction = "right"
        self.invincible = 0  # Frames d'invincibilité après avoir été touché
        self.combo_count = 0  # Compteur de combo
        self.last_attack_time = 0  # Pour gérer les combos
        
        self.player_num = player_num
        self.facing_right = True if player_num == 1 else False
        self.jump_pressed = False  # Nouvel attribut pour suivre l'état de la touche de saut
        
        # Initialiser le gestionnaire de sons
        self.sound_manager = SoundManager()
        
        # États des attaques
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None
        self.attack_rect = pygame.Rect(0, 0, 50, 50)
        self.attack_direction = "right"
        
        # Cooldowns spécifiques pour chaque type d'attaque
        self.light_attack_cooldown = 0
        self.heavy_attack_cooldown = 0
        self.special_attack_cooldown = 0
        
        # États des touches
        self.light_attack_pressed = False
        self.heavy_attack_pressed = False
        self.special_attack_pressed = False

    def update(self, obstacles):
        # Mettre à jour l'animation
        self.sprite_manager.update(1)
        
        # Mise à jour des cooldowns
        if self.light_attack_cooldown > 0:
            self.light_attack_cooldown -= 1
        if self.heavy_attack_cooldown > 0:
            self.heavy_attack_cooldown -= 1
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
                self.attack_type = None
                # Forcer la réinitialisation de l'animation
                if self.velocity.y != 0:
                    self.sprite_manager.set_animation("jump", force=True)
                elif abs(self.velocity.x) > 0:
                    self.sprite_manager.set_animation("run", force=True)
                else:
                    self.sprite_manager.set_animation("idle", force=True)
        
        # Déterminer l'animation en fonction de l'état
        if self.is_attacking:
            if self.attack_type == "light":
                self.sprite_manager.set_animation("attack1")
            elif self.attack_type == "heavy":
                self.sprite_manager.set_animation("attack2")
            elif self.attack_type == "special":
                self.sprite_manager.set_animation("attack3")
        elif self.velocity.y != 0:  # En l'air (saut ou chute)
            self.sprite_manager.set_animation("jump")
        elif abs(self.velocity.x) > 0:
            self.sprite_manager.set_animation("run")
        else:
            self.sprite_manager.set_animation("idle")
        
        # Mettre à jour l'orientation du sprite
        self.sprite_manager.set_flip(not self.facing_right)
        
        # Application de la gravité
        self.velocity += self.acceleration
        
        # Mise à jour de la position
        self.rect.x += self.velocity.x
        self.check_collision(obstacles, 'x')
        self.rect.y += self.velocity.y
        self.check_collision(obstacles, 'y')
        
        # Contrôles
        keys = pygame.key.get_pressed()
        if self.player_num == 1:
            self.handle_player1_input(keys)
        else:
            self.handle_player2_input(keys)
            
        # Mise à jour du rectangle d'attaque
        self.update_attack_rect()
        
        if self.invincible > 0:
            self.invincible -= 1
        
        # Réinitialisation du combo si trop de temps s'est écoulé
        if pygame.time.get_ticks() - self.last_attack_time > 1000:  # 1 seconde
            self.combo_count = 0

         # Mort si le joueur tombe
        if self.rect.y >= 700:
            self.health = 0
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.is_dead = True
                self.health = 0
                self.acceleration.y = 1.5
            
        

    def handle_player1_input(self, keys):
        # Mouvement horizontal
        if keys[pygame.K_q]:
            self.velocity.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.velocity.x = self.speed
            self.facing_right = True
        else:
            self.velocity.x = 0
            
        # Gestion du saut
        if keys[pygame.K_z]:
            if not self.jump_pressed:
                self.jump()
            self.jump_pressed = True
        else:
            self.jump_pressed = False

        # Attaques
        if keys[pygame.K_s] and not self.light_attack_pressed:  # Attaque légère
            self.attack("light")
            self.light_attack_pressed = True
        elif not keys[pygame.K_s]:
            self.light_attack_pressed = False
            
        if keys[pygame.K_a] and not self.heavy_attack_pressed:  # Attaque lourde
            self.attack("heavy")
            self.heavy_attack_pressed = True
        elif not keys[pygame.K_a]:
            self.heavy_attack_pressed = False
            
        if keys[pygame.K_e] and not self.special_attack_pressed:  # Attaque spéciale
            self.attack("special")
            self.special_attack_pressed = True
        elif not keys[pygame.K_e]:
            self.special_attack_pressed = False

    def handle_player2_input(self, keys):
        # Mouvement horizontal
        if keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.facing_right = True
        else:
            self.velocity.x = 0
            
        # Gestion du saut
        if keys[pygame.K_UP]:
            if not self.jump_pressed:
                self.jump()
            self.jump_pressed = True
        else:
            self.jump_pressed = False

        # Attaques
        if keys[pygame.K_RETURN] and not self.light_attack_pressed:  # Attaque légère
            self.attack("light")
            self.light_attack_pressed = True
        elif not keys[pygame.K_RETURN]:
            self.light_attack_pressed = False
            
        if keys[pygame.K_DOWN] and not self.heavy_attack_pressed:  # Attaque lourde
            self.attack("heavy")
            self.heavy_attack_pressed = True
        elif not keys[pygame.K_DOWN]:
            self.heavy_attack_pressed = False
            
        if keys[pygame.K_RSHIFT] and not self.special_attack_pressed:  # Attaque spéciale
            self.attack("special")
            self.special_attack_pressed = True
        elif not keys[pygame.K_RSHIFT]:
            self.special_attack_pressed = False

    def jump(self):
        # Vérification si le joueur est au sol
        if self.velocity.y == 0:
            self.velocity.y = self.jump_power
            self.can_double_jump = True
            self.sound_manager.play_sound('jump')
        # Double saut
        elif self.can_double_jump:
            self.velocity.y = self.jump_power
            self.can_double_jump = False
            self.sound_manager.play_sound('jump')

    def attack(self, attack_type):
        current_time = pygame.time.get_ticks()
        
        # Vérifier le cooldown spécifique au type d'attaque
        if attack_type == "light" and self.light_attack_cooldown > 0:
            return
        elif attack_type == "heavy" and self.heavy_attack_cooldown > 0:
            return
        elif attack_type == "special" and self.special_attack_cooldown > 0:
            return
        
        if self.is_attacking:  # Ne pas interrompre une attaque en cours
            return
            
        # Jouer le son d'attaque
        self.sound_manager.play_sound('attack')
        
        # Gestion des combos
        if current_time - self.last_attack_time < 500:
            self.combo_count += 1
        else:
            self.combo_count = 0
            
        self.last_attack_time = current_time
        self.is_attacking = True
        self.attack_type = attack_type
        
        # Configuration des attaques
        if attack_type == "light":
            self.attack_cooldown = 20
            self.light_attack_cooldown = 30
            self.sprite_manager.set_animation("attack1", force=True)
        elif attack_type == "heavy":
            self.attack_cooldown = 35
            self.heavy_attack_cooldown = 45
            self.sprite_manager.set_animation("attack2", force=True)
        elif attack_type == "special":
            self.attack_cooldown = 50
            self.special_attack_cooldown = 60
            self.sprite_manager.set_animation("attack3", force=True)
        else:
            return

        # Mettre à jour immédiatement le rectangle d'attaque
        self.update_attack_rect()

    def get_attack_damage(self):
        base_damage = {
            "light": 5,
            "heavy": 10,
            "special": 15
        }
        
        # Bonus de combo
        combo_multiplier = min(1 + (self.combo_count * 0.2), 2.0)  # Max 2x damage
        return base_damage.get(self.attack_type, 0) * combo_multiplier

    def take_damage(self, amount):
        if self.invincible > 0 or self.is_dead:
            return
            
        self.health -= amount
        
        # Jouer le son de dégât
        self.sound_manager.play_sound('hurt')
        
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.is_dead = True
                self.health = 0
                self.acceleration.y = 1.5
                # Jouer le son de mort
                self.sound_manager.play_sound('death')
        
        # Période d'invincibilité après avoir été touché
        self.invincible = 30
        
        # Knockback
        knockback_force = amount * 0.5
        self.velocity.y = -knockback_force
        self.velocity.x = knockback_force * (-1 if self.facing_right else 1)

    def respawn(self):
        self.health = 100
        self.rect.x, self.rect.y = self.respawn_pos
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.5)  # Activer la gravité immédiatement
        self.is_spawning = False  # Ne pas activer l'état de spawn
        self.invincible = 60
        
        # Réinitialiser les états d'attaque
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None
        self.combo_count = 0

    def update_attack_rect(self):
        """Met à jour la position du rectangle d'attaque"""
        if self.is_attacking:
            # Ajuster la taille en fonction du type d'attaque
            if self.attack_type == "light":
                width, height = 60, 40
            elif self.attack_type == "heavy":
                width, height = 70, 50
            elif self.attack_type == "special":
                width, height = 80, 60
            else:
                width, height = 50, 50
            
            self.attack_rect.size = (width, height)
            
            # Positionner le rectangle d'attaque
            if self.facing_right:
                self.attack_rect.midleft = self.rect.midright
            else:
                self.attack_rect.midright = self.rect.midleft

    def check_collision(self, obstacles, direction):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if direction == 'x':
                    # Au lieu de téléporter, on arrête simplement le mouvement
                    self.velocity.x = 0
                elif direction == 'y':
                    # Collision verticale uniquement quand on tombe
                    if self.velocity.y > 0:
                        # On ne bloque que si on est au-dessus de la plateforme
                        if self.rect.bottom - self.velocity.y <= obstacle.top + 10:
                            self.rect.bottom = obstacle.top
                            self.velocity.y = 0
                    # On ne bloque plus les collisions vers le haut
                    # elif self.velocity.y < 0:
                    #     self.rect.top = obstacle.bottom
                    #     self.velocity.y = 0

    def draw(self, screen):
        current_sprite = self.sprite_manager.get_current_sprite()
        if current_sprite:
            screen.blit(current_sprite, self.rect)
        
        # Debug: affichage du rectangle d'attaque
        if self.is_attacking:
            pygame.draw.rect(screen, (255, 0, 0), self.attack_rect, 2) 