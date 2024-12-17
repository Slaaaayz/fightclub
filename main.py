import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import random

pygame.init()
screen_info = pygame.display.Info()
print(screen_info)
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)

tmx_data = load_pygame("map.tmx")
original_width, original_height = 1200, 736
map_surface = pygame.Surface((original_width, original_height))

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_data.get_tile_image_by_gid(gid)
            if tile:
                map_surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

screen_width, screen_height = screen_info.current_w, screen_info.current_h
scaled_surface = pygame.transform.scale(map_surface, (screen_width, screen_height))

scale_x = screen_width / original_width
scale_y = screen_height / original_height

spawn_layer = tmx_data.get_object_by_name("playerSpawn1")
spawn_layer2 = tmx_data.get_object_by_name("playerSpawn2")
spawn_layer3 = tmx_data.get_object_by_name("playerSpawn3")
spawn_layer4 = tmx_data.get_object_by_name("playerSpawn4")

random_spawn = random.choice([spawn_layer, spawn_layer2, spawn_layer3, spawn_layer4])
print(random_spawn)

spawn_x = int(random_spawn.x * scale_x)
spawn_y = int(random_spawn.y * scale_y)

player_image = pygame.image.load("player.png")
player_rect = player_image.get_rect(center=(spawn_x, spawn_y))

player_speed = 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

    screen.blit(scaled_surface, (0, 0))
    screen.blit(player_image, player_rect)

    pygame.display.flip()

pygame.quit()
