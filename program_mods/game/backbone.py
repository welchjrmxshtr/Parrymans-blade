import pygame

from .settings import WIDTH, HEIGHT, FPS, BG_COLOR, WINDOW_TITLE, MESSAGE_COLOR, MESSAGE_TIME, FADE_TIME
from .input import handle_events, get_movement
from .font import make_font
from .fade import fade_to_black, fade_from_black
from .. import level
from ..player import Player
from ..camera import Camera
from ..checkpoint import Checkpoint
from ..hud import draw_hud
from ..worlds import WORLDS
from ..platform import build_deck
from ..backdrop import build_decor
from ..victory import run_victory_scene


def backbone():
    from ..start_screen import run_start_screen

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    clock = pygame.time.Clock()
    font = make_font(36)

    while True:
        if not run_start_screen(screen):
            break
        outcome = _run_game(screen, clock, font)
        if outcome == "quit":
            break

    pygame.quit()


def _run_game(screen, clock, font):
    from ..pause_menu import run_pause_menu

    level.set_level(0, 0)
    world_index = 0
    level_index = 0
    respawn_at_checkpoint = False
    entering = False
    hud_font = make_font(20)

    while True:
        decks = {plat.size: build_deck(*plat.size) for plat in level.PLATFORMS}
        decor_surf = build_decor(level.LEVEL_WIDTH, level.LEVEL_HEIGHT, level.PLATFORMS, level.DECOR)
        solid_furniture = set(level.DECOR.get("furniture", {})) if level.DECOR else set()
        player = Player(*level.PLAYER_SPAWN)
        camera = Camera(WIDTH, HEIGHT, level.LEVEL_WIDTH, level.LEVEL_HEIGHT)
        checkpoint = Checkpoint(*level.CHECKPOINT_POS)
        spawn = level.PLAYER_SPAWN
        if respawn_at_checkpoint:
            checkpoint.activate()
            spawn = (checkpoint.rect.centerx, checkpoint.rect.bottom - Player.HEIGHT // 2)
            player = Player(*spawn)
            respawn_at_checkpoint = False
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
                    player = Player(*level.PLAYER_SPAWN)
                    camera = Camera(WIDTH, HEIGHT, level.LEVEL_WIDTH, level.LEVEL_HEIGHT)
                    checkpoint = Checkpoint(*level.CHECKPOINT_POS)
                    spawn = level.PLAYER_SPAWN
                    message_timer = 0.0

            running = handle_events(events, player)
            if not running:
                return "quit"

            keys = pygame.key.get_pressed()
            player.move(*get_movement(keys))
            player.update(level.PLATFORMS, dt)

            if checkpoint.rect.colliderect(player.rect):
                if not checkpoint.activated:
                    checkpoint.activate()
                    spawn = (checkpoint.rect.centerx, checkpoint.rect.bottom - Player.HEIGHT // 2)
                    message_timer = MESSAGE_TIME

            if player.rect.top > level.LEVEL_HEIGHT + 100:
                player = Player(*spawn)

            if message_timer > 0.0:
                message_timer -= dt

            camera.follow(player.rect)

            screen.fill(BG_COLOR)
            for plat in level.PLATFORMS:
                if plat.height > 30 and (plat.left, plat.top, plat.width, plat.height) in solid_furniture:
                    continue
                screen.blit(decks[plat.size], camera.apply(plat))
            if decor_surf is not None:
                screen.blit(decor_surf, camera.apply(decor_surf.get_rect()))
            checkpoint.draw(screen, camera.apply(checkpoint.rect))
            player.draw(screen, camera.apply(player.rect))
            draw_hud(screen, hud_font, level)
            if message_timer > 0.0:
                text = font.render("Checkpoint reached!", MESSAGE_COLOR)
                screen.blit(text, text.get_rect(center=(WIDTH // 2, 40)))
            pygame.display.flip()

            if entering:
                fade_from_black(screen, FADE_TIME)
                entering = False

            if checkpoint.activated and player.rect.left >= level.LEVEL_WIDTH:
                fade_to_black(screen, FADE_TIME)
                run_victory_scene(screen)
                if level_index + 1 < len(level.WORLD["levels"]):
                    level_index += 1
                    level.set_level(world_index, level_index)
                elif world_index + 1 < len(WORLDS):
                    world_index += 1
                    level_index = 0
                    level.set_level(world_index, level_index)
                else:
                    respawn_at_checkpoint = True
                entering = True
                break
