import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scroll = pygame.Vector2(0, 0)

    def update(self, player1, player2):
        pass

    def apply(self, rect):
        return pygame.Rect(
            rect.x,
            rect.y,
            rect.width,
            rect.height
        )

    def apply_to_pos(self, pos):
        return pos 