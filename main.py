import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import random

pygame.init()
screen_info = pygame.display.Info()
screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)

tmx_data = load_pygame("map.tmx")
map_surface = pygame.Surface((1200, 736))

for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid in layer:
            tile = tmx_data.get_tile_image_by_gid(gid)
            if tile:
                map_surface.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

scaled_surface = pygame.transform.scale(map_surface, (screen_info.current_w, screen_info.current_h))



spawn_layer = tmx_data.get_object_by_name("playerSpawn1")
spawn_layer2 = tmx_data.get_object_by_name("playerSpawn2")
spawn_layer3 = tmx_data.get_object_by_name("playerSpawn3")
spawn_layer4 = tmx_data.get_object_by_name("playerSpawn4")

random_spawn = random.choice([spawn_layer, spawn_layer2, spawn_layer3, spawn_layer4])
print(random_spawn)

player_image = pygame.image.load("player.png").convert_alpha()
player_rect = player_image.get_rect(center=(random_spawn.x, random_spawn.y))

player_speed = 5

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_q]:
    #     player_rect.x -= player_speed
    # if keys[pygame.K_d]:
    #     player_rect.x += player_speed

    screen.blit(scaled_surface, (0, 0))
    screen.blit(player_image, player_rect)

    pygame.display.flip()

pygame.quit()
