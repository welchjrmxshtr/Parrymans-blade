import pygame


class Camera:
    def __init__(self, view_w, view_h, world_w, world_h):
        self.view = pygame.Rect(0, 0, view_w, view_h)
        self.world = pygame.Rect(0, 0, world_w, world_h)
        self.offset = pygame.Vector2(0, 0)

    def follow(self, target):
        self.offset.x = target.centerx - self.view.w / 2
        self.offset.y = target.centery - self.view.h / 2
        self.offset.x = max(self.world.left, min(self.offset.x, self.world.right - self.view.w))
        self.offset.y = max(self.world.top, min(self.offset.y, self.world.bottom - self.view.h))

    def apply(self, rect):
        return rect.move(-round(self.offset.x), -round(self.offset.y))
