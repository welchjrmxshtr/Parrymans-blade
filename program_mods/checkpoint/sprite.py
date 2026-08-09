import pygame

FLAG_INACTIVE = 0
FLAG_ACTIVE = 1

_PALETTE = {
    "P": (190, 195, 205),
    "D": (135, 140, 150),
    "G": (165, 170, 180),
    "A": (80, 220, 110),
}

_FLAG_PIXELS = [
    "..PDGGGGGGGGG",
    "..PDGGGGGGGG.",
    "..PDGGGGGGG..",
    "..PDGGGGGG...",
    "..PDGGGGG....",
    "..PDGGGG.....",
]

_POLE_PIXELS = [
    "..PD.........",
    "..PD.........",
]

_BASE_PIXELS = [
    ".PPPP........",
    ".PPPP........",
]


def _pixels(state):
    flag = "A" if state == FLAG_ACTIVE else "G"
    rows = [line.replace("G", flag) for line in _FLAG_PIXELS]
    rows += _POLE_PIXELS * 10
    rows += _BASE_PIXELS
    return rows


def build_sprite(state=FLAG_INACTIVE, scale=2):
    pixels = _pixels(state)
    h = len(pixels)
    w = len(pixels[0])
    surf = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA)
    for row, line in enumerate(pixels):
        for col, ch in enumerate(line):
            color = _PALETTE.get(ch)
            if color is None:
                continue
            pygame.draw.rect(surf, color, (col * scale, row * scale, scale, scale))
    return surf
