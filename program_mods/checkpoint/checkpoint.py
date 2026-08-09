import pygame

from .sprite import build_sprite, FLAG_INACTIVE, FLAG_ACTIVE


class Checkpoint:
    WIDTH = 26
    HEIGHT = 56

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.midbottom = (x, y)
        self.activated = False
        self.frames = [build_sprite(FLAG_INACTIVE), build_sprite(FLAG_ACTIVE)]

    def activate(self):
        if not self.activated:
            self.activated = True

    def draw(self, screen, pos):
        screen.blit(self.frames[self.activated], pos)
