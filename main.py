import pygame
import os 
from pytmx import load_pygame, TiledTileLayer


pygame.init()

os.environ["SDL_VIDEO_WINDOWS_POS"] = "0 , 28"

screen = pygame.display.set_mode((0,0), FULLSCREEN)

gameloop = True
tmxdata = load_pygame("map.tmx")

while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            gameloop = False

pygame.quit()
