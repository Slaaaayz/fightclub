import pygame
import os
from pytmx import load_pygame, TiledTileLayer

pygame.init()

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,28"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

tmx_data = load_pygame("./map.tsx")

gameloop = True
while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gameloop = False

    for layer in tmx_data.visible_layers:
        if isinstance(layer, TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tmx_data.tilewidth, y * tmx_data.tileheight))

    pygame.display.flip()  

pygame.quit()
