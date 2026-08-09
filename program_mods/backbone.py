import pygame

from .player import Player
from .camera import Camera
from .level import LEVEL_WIDTH, LEVEL_HEIGHT, PLAYER_SPAWN, PLATFORMS

WIDTH, HEIGHT = 960, 540
FPS = 60
BG_COLOR = (30, 30, 45)
PLATFORM_COLOR = (90, 140, 220)


def backbone():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Platformer")
    clock = pygame.time.Clock()

    player = Player(*PLAYER_SPAWN)
    camera = Camera(WIDTH, HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    player.jump_pressed()
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    player.jump_released()

        keys = pygame.key.get_pressed()
        player.move(keys[pygame.K_LEFT] or keys[pygame.K_a],
                    keys[pygame.K_RIGHT] or keys[pygame.K_d])
        player.update(PLATFORMS, dt)

        if player.rect.top > LEVEL_HEIGHT + 100:
            player = Player(*PLAYER_SPAWN)

        camera.follow(player.rect)

        screen.fill(BG_COLOR)
        for plat in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, camera.apply(plat))
        player.draw(screen, camera.apply(player.rect))
        pygame.display.flip()

    pygame.quit()
