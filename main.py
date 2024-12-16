import pygame
import os

pygame.init()

os.environ["SDL_VIDEO_WINDOW_POS"] = "0,28"

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

gameloop = True
while gameloop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameloop = False
        if event.type == pygame.KEYDOWN:
            gameloop = False

pygame.quit()
