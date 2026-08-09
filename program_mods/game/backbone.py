import pygame

from .settings import WIDTH, HEIGHT, FPS, BG_COLOR, WINDOW_TITLE, MESSAGE_COLOR, MESSAGE_TIME
from .input import handle_events, get_movement
from .font import make_font
from ..player import Player
from ..camera import Camera
from ..checkpoint import Checkpoint
from ..level import PLATFORMS, PLAYER_SPAWN, CHECKPOINT_POS, LEVEL_WIDTH, LEVEL_HEIGHT
from ..platform import build_deck


def backbone():
    from ..start_screen import run_start_screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = make_font(36)
    decks = {plat.size: build_deck(*plat.size) for plat in PLATFORMS}

    while True:
        if not run_start_screen(screen):
            break
        outcome = _run_game(screen, clock, font, decks)
        if outcome == "quit":
            break

    pygame.quit()


def _run_game(screen, clock, font, decks):
    from ..pause_menu import run_pause_menu

    player = Player(*PLAYER_SPAWN)
    camera = Camera(WIDTH, HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)
    checkpoint = Checkpoint(*CHECKPOINT_POS)
    spawn = PLAYER_SPAWN
    message_timer = 0.0

    while True:
        dt = min(clock.tick(FPS) / 1000.0, 1 / 20.0)

        paused = False
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = True

        if paused:
            action = run_pause_menu(screen)
            if action == "quit":
                return "quit"
            if action == "title":
                return "title"
            if action == "restart":
                player = Player(*PLAYER_SPAWN)
                camera = Camera(WIDTH, HEIGHT, LEVEL_WIDTH, LEVEL_HEIGHT)
                checkpoint = Checkpoint(*CHECKPOINT_POS)
                spawn = PLAYER_SPAWN
                message_timer = 0.0

        running = handle_events(events, player)
        if not running:
            return "quit"

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
            screen.blit(decks[plat.size], camera.apply(plat))
        checkpoint.draw(screen, camera.apply(checkpoint.rect))
        player.draw(screen, camera.apply(player.rect))
        if message_timer > 0.0:
            text = font.render("Checkpoint reached!", MESSAGE_COLOR)
            screen.blit(text, text.get_rect(center=(WIDTH // 2, 40)))
        pygame.display.flip()
