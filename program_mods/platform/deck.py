import pygame

WOOD_LIGHT = (146, 116, 80)
WOOD_BASE = (122, 94, 62)
WOOD_DARK = (108, 82, 54)
SEAM = (62, 45, 30)
NAIL = (84, 62, 40)
EDGE = (40, 28, 18)

PLANK_H = 26
JOINT_W = 56
JOINT_STAGGER = 28

_cache = {}


def build_deck(w, h):
    key = (w, h)
    if key in _cache:
        return _cache[key]

    surf = pygame.Surface((w, h))
    plank_row = 0
    y = 0
    while y < h:
        row_h = min(PLANK_H, h - y)
        base = WOOD_BASE if plank_row % 2 == 0 else WOOD_DARK
        pygame.draw.rect(surf, base, (0, y, w, row_h))
        pygame.draw.line(surf, WOOD_LIGHT, (0, y), (w, y))
        pygame.draw.line(surf, SEAM, (0, y + row_h - 1), (w, y + row_h - 1))
        offset = JOINT_STAGGER if plank_row % 2 else 0
        for x in range(offset, w - 3, JOINT_W):
            jx = x + 2
            pygame.draw.rect(surf, SEAM, (jx, y + 2, 2, row_h - 4))
            pygame.draw.rect(surf, NAIL, (jx - 1, y + 3, 2, 2))
        plank_row += 1
        y += PLANK_H

    pygame.draw.rect(surf, EDGE, (0, h - 2, w, 2))
    _cache[key] = surf
    return surf
