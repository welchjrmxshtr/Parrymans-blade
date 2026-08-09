import pygame

_PLAYER_PIXELS = [
    "..HHHHHHHHHHHHH..",
    "..HHHHHHHHHHHHH..",
    ".HHHHHHHHHHHHHHH.",
    ".HHSSSSSSSSSSSHH.",
    ".HHSSSSSSSSSSSHH.",
    ".HSSSSSSSSSSSSSH.",
    ".HSSSSSSSSSSSSSH.",
    ".HSSSSSSSSSSSSSH.",
    ".HSSEESSSSEESSSH.",
    ".HSSSSSMMSSSSSSH.",
    ".HHHSSSSSSSSSHHH.",
    ".TTTTTTTTTTTTTTT.",
    "TTTTTTTTTTTTTTTTT",
    "TTTTTTTTTTTTTTTTT",
    ".TTTTTTTTTTTTTTT.",
    "..TTTTTTTTTTTTT..",
    ".PPPPPPPPPPPPPPP.",
    "..PP.........PP..",
    "..PP.........PP..",
    "..PP.........PP..",
    "..PP.........PP..",
    "..KK.........KK..",
    ".KKK.........KKK.",
]

_PALETTE = {
    "H": (74, 47, 27),
    "S": (255, 212, 163),
    "E": (24, 20, 20),
    "M": (120, 60, 40),
    "T": (224, 83, 61),
    "P": (61, 90, 128),
    "K": (43, 43, 43),
}


def build_sprite(scale=2):
    h = len(_PLAYER_PIXELS)
    w = len(_PLAYER_PIXELS[0])
    surf = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA)
    for row, line in enumerate(_PLAYER_PIXELS):
        for col, ch in enumerate(line):
            color = _PALETTE.get(ch)
            if color is None:
                continue
            pygame.draw.rect(surf, color, (col * scale, row * scale, scale, scale))
    return surf
