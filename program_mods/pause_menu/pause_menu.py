import pygame

from ..game.settings import WIDTH, HEIGHT
from ..game.font import make_font

TITLE = "PAUSED"
TITLE_COLOR = (214, 208, 196)
OVERLAY_COLOR = (10, 10, 18, 180)
ITEM_BG = (60, 55, 80)
ITEM_SELECTED_BG = (110, 100, 150)
ITEM_COLOR = (150, 150, 170)
ITEM_SELECTED_COLOR = (240, 236, 224)
HINT_COLOR = (110, 110, 130)

MENU_ITEMS = ("Resume", "Restart", "Quit to Title", "Quit to Desktop")
_ACTIONS = ("resume", "restart", "title", "quit")

FONT_TITLE = 48
FONT_ITEM = 30
FONT_HINT = 20

_NAV_UP = (pygame.K_UP, pygame.K_w)
_NAV_DOWN = (pygame.K_DOWN, pygame.K_s)
_SELECT_KEYS = (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE)


def run_pause_menu(screen):
    font_title = make_font(FONT_TITLE)
    font_item = make_font(FONT_ITEM)
    font_hint = make_font(FONT_HINT)

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)

    title = font_title.render(TITLE, TITLE_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, 130))
    hint = font_hint.render("ARROWS/W/S to choose    ENTER to select    ESC to resume", HINT_COLOR)
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT - 40))

    item_rects = []
    for i in range(len(MENU_ITEMS)):
        r = pygame.Rect(0, 0, 380, 46)
        r.center = (WIDTH // 2, 240 + i * 58)
        item_rects.append(r)

    clock = pygame.time.Clock()
    selected = 0

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"
                if event.key in _NAV_UP:
                    selected = (selected - 1) % len(MENU_ITEMS)
                elif event.key in _NAV_DOWN:
                    selected = (selected + 1) % len(MENU_ITEMS)
                elif event.key in _SELECT_KEYS:
                    return _ACTIONS[selected]

        screen.blit(overlay, (0, 0))
        screen.blit(title, title_rect)
        for i, item in enumerate(MENU_ITEMS):
            rect = item_rects[i]
            is_selected = i == selected
            pygame.draw.rect(screen, ITEM_SELECTED_BG if is_selected else ITEM_BG, rect, border_radius=8)
            text = font_item.render(item, ITEM_SELECTED_COLOR if is_selected else ITEM_COLOR)
            screen.blit(text, text.get_rect(center=rect.center))
        screen.blit(hint, hint_rect)
        pygame.display.flip()
