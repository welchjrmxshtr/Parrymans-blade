import pygame

from .settings import WIDTH, HEIGHT, FPS, BG_COLOR, PLATFORM_COLOR, WINDOW_TITLE, MESSAGE_COLOR, MESSAGE_TIME
from .input import handle_events, get_movement
from .font import make_font
from ..player import Player
from ..camera import Camera
from ..checkpoint import Checkpoint
from ..level import PLATFORMS, PLAYER_SPAWN, CHECKPOINT_POS, LEVEL_WIDTH, LEVEL_HEIGHT


def backbone():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = make_font(36)

    player = Player(*PLAYER_SPAWN)
    camera = Camera(WIDTH, HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)
    checkpoint = Checkpoint(*CHECKPOINT_POS)
    spawn = PLAYER_SPAWN
    message_timer = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        running = handle_events(pygame.event.get(), player)

        keys = pygame.key.get_pressed()
        player.move(*get_movement(keys))
        player.update(PLATFORMS, dt)

        if checkpoint.rect.colliderect(player.rect):
            if not checkpoint.activated:
                checkpoint.activate()
                spawn = (checkpoint.rect.centerx, checkpoint.rect.bottom - Player.HEIGHT // 2)
                message_timer = MESSAGE_TIME

        if player.rect.top > LEVEL_HEIGHT + 100:
            player = Player(*spawn)

        if message_timer > 0.0:
            message_timer -= dt

        camera.follow(player.rect)

        screen.fill(BG_COLOR)
        for plat in PLATFORMS:
            pygame.draw.rect(screen, PLATFORM_COLOR, camera.apply(plat))
        checkpoint.draw(screen, camera.apply(checkpoint.rect))
        player.draw(screen, camera.apply(player.rect))
        if message_timer > 0.0:
            text = font.render("Checkpoint reached!", MESSAGE_COLOR)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 40)))
        pygame.display.flip()

    pygame.quit()
