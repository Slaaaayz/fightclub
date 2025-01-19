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
        self.acceleration = pygame.math.Vector2(0, 0.5)  # Gravité
        self.speed = 5
        self.jump_power = -12
        self.can_double_jump = True
        self.is_spawning = True  # Nouvel attribut pour l'état de spawn
        
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

    def update(self, obstacles):
        # Mettre à jour l'animation
        self.sprite_manager.update(1)
        
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
        
        # Si en état de spawn, attendre un mouvement pour commencer à tomber
        if self.is_spawning:
            keys = pygame.key.get_pressed()
            if (self.player_num == 1 and (keys[pygame.K_q] or keys[pygame.K_d] or keys[pygame.K_z])) or \
               (self.player_num == 2 and (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_UP])):
                self.is_spawning = False
            else:
                return  # Ne pas appliquer la gravité tant qu'on est en spawn

        # Mise à jour des cooldowns
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            if self.attack_cooldown == 0:
                self.is_attacking = False
                self.attack_type = None
                
        if self.invincible > 0:
            self.invincible -= 1
            
        # Réinitialisation du combo si trop de temps s'est écoulé
        if pygame.time.get_ticks() - self.last_attack_time > 1000:  # 1 seconde
            self.combo_count = 0

        # Application de la gravité
        self.velocity += self.acceleration
        
        # Augmentation de la gravité si la santé est faible
        if self.health < 30:
            self.velocity.y += 0.2
            
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
            if not self.jump_pressed:  # Seulement si la touche n'était pas déjà pressée
                self.jump()
            self.jump_pressed = True
        else:
            self.jump_pressed = False  # Réinitialisation quand la touche est relâchée

        # Attaques
        if keys[pygame.K_s]:  # Attaque légère
            self.attack("light")
        elif keys[pygame.K_a]:  # Attaque lourde
            self.attack("heavy")
        elif keys[pygame.K_e]:  # Attaque spéciale
            self.attack("special")

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
            if not self.jump_pressed:  # Seulement si la touche n'était pas déjà pressée
                self.jump()
            self.jump_pressed = True
        else:
            self.jump_pressed = False  # Réinitialisation quand la touche est relâchée

        # Attaques
        if keys[pygame.K_RETURN]:  # Attaque légère avec Entrée
            self.attack("light")
        elif keys[pygame.K_DOWN]:  # Attaque lourde avec flèche bas
            self.attack("heavy")
        elif keys[pygame.K_RSHIFT]:  # Attaque spéciale avec Shift droit
            self.attack("special")

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
        
        if self.attack_cooldown > 0:
            return
            
        # Jouer le son d'attaque
        self.sound_manager.play_sound('attack')
        
        # Gestion des combos
        if current_time - self.last_attack_time < 500:  # Fenêtre de 0.5 seconde pour les combos
            self.combo_count += 1
        else:
            self.combo_count = 0
            
        self.last_attack_time = current_time
        self.is_attacking = True
        self.attack_type = attack_type
        
        # Configuration des attaques
        if attack_type == "light":
            self.attack_cooldown = 15  # Frames
            self.attack_rect.size = (60, 40)
        elif attack_type == "heavy":
            self.attack_cooldown = 30
            self.attack_rect.size = (70, 50)
        elif attack_type == "special" and self.combo_count >= 2:
            self.attack_cooldown = 45
            self.attack_rect.size = (80, 60)
        else:
            return

        self.attack_direction = "right" if self.facing_right else "left"

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
        self.health = 100  # Réinitialiser la santé
        self.rect.x, self.rect.y = self.respawn_pos  # Retour au point de spawn
        self.velocity = pygame.math.Vector2(0, 0)  # Réinitialiser la vélocité
        self.is_spawning = True  # Remettre en état de spawn
        self.invincible = 60  # Invincibilité plus longue au respawn

    def update_attack_rect(self):
        if self.is_attacking:
            if self.attack_direction == "right":
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