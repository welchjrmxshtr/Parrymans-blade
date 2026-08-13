import pygame

from ..game.settings import WIDTH, HEIGHT, BG_COLOR
from ..game.font import make_font
from ..player.sprite import build_sprite, FRAME_IDLE, FRAME_RUN_A, FRAME_RUN_B

TITLE = "REAPER'S DECK"
TITLE_COLOR = (214, 208, 196)
SUBTITLE = "A float through the underworld"
SUBTITLE_COLOR = (150, 148, 170)
PROMPT = "Press ENTER to start"
PROMPT_COLOR = (140, 210, 160)
HINT = "A/D or arrows to move   |   SPACE to jump   |   ESC to quit"
HINT_COLOR = (105, 105, 128)

_FLOAT_SEQ = (FRAME_RUN_A, FRAME_IDLE, FRAME_RUN_B, FRAME_IDLE)
_FLOAT_TIME = 0.2
_BLINK_TIME = 0.5

FONT_TITLE = 64
FONT_SUB = 26
FONT_PROMPT = 32
FONT_HINT = 20
MASCOT_SCALE = 2

_START_KEYS = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)


def run_start_screen(screen):
    font_title = make_font(FONT_TITLE)
    font_sub = make_font(FONT_SUB)
    font_prompt = make_font(FONT_PROMPT)
    font_hint = make_font(FONT_HINT)

    frames = [build_sprite(f, MASCOT_SCALE) for f in _FLOAT_SEQ]
    shadow = pygame.Surface((frames[0].get_width() + 16, 20), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow, (0, 0, 0, 90), shadow.get_rect())

    clock = pygame.time.Clock()
    anim = 0
    anim_timer = 0.0
    blink = 0.0

    while True:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key in _START_KEYS:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False

        anim_timer += dt
        if anim_timer >= _FLOAT_TIME:
            anim_timer -= _FLOAT_TIME
            anim = (anim + 1) % len(_FLOAT_SEQ)
        blink += dt
        if blink >= _BLINK_TIME * 2:
            blink -= _BLINK_TIME * 2

        screen.fill(BG_COLOR)
        title = font_title.render(TITLE, TITLE_COLOR)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 120)))
        sub = font_sub.render(SUBTITLE, SUBTITLE_COLOR)
        screen.blit(sub, sub.get_rect(center=(WIDTH // 2, 175)))

        surf = frames[anim]
        rect = surf.get_rect(center=(WIDTH // 2, 300))
        rect.top -= getattr(surf, "body_top", 0)
        screen.blit(shadow, (rect.centerx - shadow.get_width() // 2, rect.bottom + 6))
        screen.blit(surf, rect)

        if blink < _BLINK_TIME:
            prompt = font_prompt.render(PROMPT, PROMPT_COLOR)
            screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, 410)))
        hint = font_hint.render(HINT, HINT_COLOR)
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 30)))

        pygame.display.flip()
