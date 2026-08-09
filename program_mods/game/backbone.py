import pygame

from .settings import WIDTH, HEIGHT, FPS, BG_COLOR, PLATFORM_COLOR, WINDOW_TITLE
from .input import handle_events, get_movement
from ..player import Player
from ..camera import Camera
from ..level import PLATFORMS, PLAYER_SPAWN, LEVEL_WIDTH, LEVEL_HEIGHT


def backbone():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()

    player = Player(*PLAYER_SPAWN)
    camera = Camera(WIDTH, HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        running = handle_events(pygame.event.get(), player)

        keys = pygame.key.get_pressed()
        player.move(*get_movement(keys))
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
