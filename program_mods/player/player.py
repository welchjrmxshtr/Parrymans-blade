import pygame

from .sprite import build_sprite, FRAME_IDLE, FRAME_RUN_A, FRAME_RUN_B


class Player:
    WIDTH = 42
    HEIGHT = 46
    MOVE_SPEED = 300.0
    JUMP_SPEED = -560.0
    GRAVITY = 1400.0
    MAX_FALL = 900.0
    COYOTE_TIME = 0.1
    JUMP_BUFFER_TIME = 0.12
    RUN_FRAME_TIME = 0.12

    def __init__(self, x, y):
        self.rect = pygame.Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.rect.center = (x, y)
        self.frames = [
            build_sprite(FRAME_IDLE),
            build_sprite(FRAME_RUN_A),
            build_sprite(FRAME_RUN_B),
        ]
        self.frame = FRAME_IDLE
        self._anim_timer = 0.0
        self.facing = 1
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = False
        self._coyote_timer = 0.0
        self._jump_buffer = 0.0

    def draw(self, screen, pos):
        surf = self.frames[self.frame]
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
        was_grounded = self.on_ground
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.vy = 0.0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                    self.vy = 0.0
        if self.vy >= 0.0 and was_grounded:
            for plat in platforms:
                if (plat.top == self.rect.bottom
                        and self.rect.right > plat.left
                        and self.rect.left < plat.right):
                    self.on_ground = True
                    break

        self._update_animation(dt)

    def _update_animation(self, dt):
        if self.vx != 0.0 and self.on_ground:
            self._anim_timer += dt
            if self._anim_timer >= self.RUN_FRAME_TIME:
                self._anim_timer = 0.0
                self.frame = FRAME_RUN_B if self.frame == FRAME_RUN_A else FRAME_RUN_A
        else:
            self.frame = FRAME_IDLE
            self._anim_timer = 0.0
