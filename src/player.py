import pygame
import math
from src.sprite_manager import SpriteManager
from src.sound_manager import SoundManager

class Player:
    def __init__(self, pos, sprite_path, player_num):
        self.sprite_manager = SpriteManager()
        try:
            self.sprite_manager.load_sprite_sheets(sprite_path)
        except Exception as e:
            print(f"Erreur lors du chargement des sprites pour le joueur {player_num}: {e}")
        
        initial_sprite = self.sprite_manager.get_current_sprite()
        if initial_sprite:
            self.rect = initial_sprite.get_rect()
        else:
            print(f"Attention: Utilisation d'un rectangle par défaut pour le joueur {player_num}")
            self.rect = pygame.Rect(0, 0, 50, 50)
        
        self.rect.x, self.rect.y = pos
        
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0.5)  
        self.speed = 5
        self.jump_power = -12
        self.can_double_jump = True
        self.is_spawning = False 
        
        self.health = 100
        self.lives = 3  
        self.respawn_pos = pos  # Sauvegarder la position de spawn
        self.is_dead = False  
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None  
        self.attack_rect = pygame.Rect(0, 0, 50, 50)
        self.attack_direction = "right"
        self.invincible = 0  # Frames d'invincibilité après avoir été touché
        self.combo_count = 0  
        self.last_attack_time = 0  
        
        self.player_num = player_num
        self.facing_right = True if player_num == 1 else False
        self.jump_pressed = False  
        
        self.sound_manager = None
        
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None
        self.attack_rect = pygame.Rect(0, 0, 50, 50)
        self.attack_direction = "right"
        
        self.light_attack_cooldown = 0
        self.heavy_attack_cooldown = 0
        self.special_attack_cooldown = 0
        
        self.light_attack_pressed = False
        self.heavy_attack_pressed = False
        self.special_attack_pressed = False

    def update(self, obstacles):
        self.sprite_manager.update(1)
        
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
                if self.velocity.y != 0:
                    self.sprite_manager.set_animation("jump", force=True)
                elif abs(self.velocity.x) > 0:
                    self.sprite_manager.set_animation("run", force=True)
                else:
                    self.sprite_manager.set_animation("idle", force=True)
        
        if self.is_attacking:
            if self.attack_type == "light":
                self.sprite_manager.set_animation("attack1")
            elif self.attack_type == "heavy":
                self.sprite_manager.set_animation("attack2")
            elif self.attack_type == "special":
                self.sprite_manager.set_animation("attack3")
        elif self.velocity.y != 0:  
            self.sprite_manager.set_animation("jump")
        elif abs(self.velocity.x) > 0:
            self.sprite_manager.set_animation("run")
        else:
            self.sprite_manager.set_animation("idle")
        
        self.sprite_manager.set_flip(not self.facing_right)
        
        self.velocity += self.acceleration
        
        self.rect.x += self.velocity.x
        self.check_collision(obstacles, 'x')
        self.rect.y += self.velocity.y
        self.check_collision(obstacles, 'y')
        
        keys = pygame.key.get_pressed()
        if self.player_num == 1:
            self.handle_player1_input(keys)
        else:
            self.handle_player2_input(keys)
            
        self.update_attack_rect()
        
        if self.invincible > 0:
            self.invincible -= 1
        
        if pygame.time.get_ticks() - self.last_attack_time > 1000:  
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
        if self.velocity.y == 0:
            self.velocity.y = self.jump_power
            self.can_double_jump = True
            if self.sound_manager:
                self.sound_manager.play_sound('jump')
        # Double saut
        elif self.can_double_jump:
            self.velocity.y = self.jump_power
            self.can_double_jump = False
            if self.sound_manager:
                self.sound_manager.play_sound('jump')

    def attack(self, attack_type):
        current_time = pygame.time.get_ticks()
        
        if attack_type == "light" and self.light_attack_cooldown > 0:
            return
        elif attack_type == "heavy" and self.heavy_attack_cooldown > 0:
            return
        elif attack_type == "special" and self.special_attack_cooldown > 0:
            return
        
        if self.is_attacking:  # Ne pas interrompre une attaque en cours
            return
            
        # Jouer le son d'attaque
        if self.sound_manager:
            self.sound_manager.play_sound('attack')
        
        if current_time - self.last_attack_time < 500:
            self.combo_count += 1
        else:
            self.combo_count = 0
            
        self.last_attack_time = current_time
        self.is_attacking = True
        self.attack_type = attack_type
        
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

        self.update_attack_rect()

    def get_attack_damage(self):
        base_damage = {
            "light": 5,
            "heavy": 10,
            "special": 15
        }
        
        combo_multiplier = min(1 + (self.combo_count * 0.2), 2.0)  
        return base_damage.get(self.attack_type, 0) * combo_multiplier

    def take_damage(self, amount):
        if self.invincible > 0 or self.is_dead:
            return
            
        self.health -= amount
        
        # Jouer le son de dégât s'il y a un sound_manager
        if self.sound_manager:
            self.sound_manager.play_sound('hurt')
        
        if self.health <= 0:
            self.lives -= 1
            if self.lives > 0:
                self.respawn()
            else:
                self.is_dead = True
                self.health = 0
                self.acceleration.y = 1.5
                # Jouer le son de mort s'il y a un sound_manager
                if self.sound_manager:
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
        self.acceleration = pygame.math.Vector2(0, 0.5)  
        self.is_spawning = False  
        self.invincible = 60
        
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_type = None
        self.combo_count = 0

    def update_attack_rect(self):
        if self.is_attacking:
            if self.attack_type == "light":
                width, height = 40, 30  
            elif self.attack_type == "heavy":
                width, height = 45, 35  
            elif self.attack_type == "special":
                width, height = 50, 40  
            else:
                width, height = 35, 35  
            
            self.attack_rect.size = (width, height)
            
            if self.facing_right:
                self.attack_rect.midleft = (self.rect.right - 10, self.rect.centery)
            else:
                self.attack_rect.midright = (self.rect.left + 10, self.rect.centery)

    def check_collision(self, obstacles, direction):
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                if direction == 'x':
                    self.velocity.x = 0
                elif direction == 'y':
                    if self.velocity.y > 0:
                        if self.rect.bottom - self.velocity.y <= obstacle.top + 10:
                            self.rect.bottom = obstacle.top
                            self.velocity.y = 0

    def draw(self, screen):
        current_sprite = self.sprite_manager.get_current_sprite()
        if current_sprite:
            screen.blit(current_sprite, self.rect)
        