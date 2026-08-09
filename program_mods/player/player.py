import pygame

from .sprite import build_sprite


class Player:
    WIDTH = 34
    HEIGHT = 46
    MOVE_SPEED = 300.0
    JUMP_SPEED = -560.0
    GRAVITY = 1400.0
    MAX_FALL = 900.0
    COYOTE_TIME = 0.1
    JUMP_BUFFER_TIME = 0.12

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (x, y)
        self.surface = build_sprite()
        self.facing = 1
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self._coyote_timer = 0.0
        self._jump_buffer = 0.0

    def draw(self, screen, pos):
        surf = self.surface
        if self.facing < 0:
            surf = pygame.transform.flip(surf, True, False)
        screen.blit(surf, pos)

    def move(self, left, right):
        self.vx = 0.0
        if left:
            self.facing = -1
            self.vx = -self.MOVE_SPEED
        elif right:
            self.facing = 1
            self.vx = self.MOVE_SPEED

    def jump_pressed(self):
        self._jump_buffer = self.JUMP_BUFFER_TIME

    def jump_released(self):
        if self.vy < 0:
            self.vy *= 0.5

    def update(self, platforms, dt):
        self._coyote_timer = max(0.0, self._coyote_timer - dt)
        self._jump_buffer = max(0.0, self._jump_buffer - dt)

        if self.on_ground:
            self._coyote_timer = self.COYOTE_TIME

        if self._jump_buffer > 0.0 and self._coyote_timer > 0.0:
            self.vy = self.JUMP_SPEED
            self.on_ground = False
            self._jump_buffer = 0.0
            self._coyote_timer = 0.0

        self.vy = min(self.vy + self.GRAVITY * dt, self.MAX_FALL)

        self.rect.x += round(self.vx * dt)
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                elif self.vx < 0:
                    self.rect.left = plat.right

        self.rect.y += round(self.vy * dt)
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                self.vy = 0.0
