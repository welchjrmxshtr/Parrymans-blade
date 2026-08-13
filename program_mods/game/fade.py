import pygame


def fade_to_black(screen, duration=1.0):
    _fade(screen, duration, 0, 255)


def fade_from_black(screen, duration=1.0):
    _fade(screen, duration, 255, 0)


def _fade(screen, duration, start, end):
    clock = pygame.time.Clock()
    overlay = pygame.Surface(screen.get_size())
    overlay.fill((0, 0, 0))
    progress = 0.0
    while progress < 1.0:
        dt = clock.tick(60) / 1000.0
        progress = min(progress + dt / max(duration, 0.001), 1.0)
        alpha = round(start + (end - start) * progress)
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
