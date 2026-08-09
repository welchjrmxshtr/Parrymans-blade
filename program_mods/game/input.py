import pygame

JUMP_KEYS = (pygame.K_SPACE, pygame.K_UP, pygame.K_w)


def handle_events(events, player):
    running = True
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key in JUMP_KEYS:
                player.jump_pressed()
        elif event.type == pygame.KEYUP:
            if event.key in JUMP_KEYS:
                player.jump_released()
    return running


def get_movement(keys):
    return (
        keys[pygame.K_LEFT] or keys[pygame.K_a],
        keys[pygame.K_RIGHT] or keys[pygame.K_d],
    )
