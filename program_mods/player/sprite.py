import pygame

FRAME_IDLE = 0
FRAME_RUN_A = 1
FRAME_RUN_B = 2

_PALETTE = {
    "H": (74, 47, 27),
    "S": (255, 212, 163),
    "E": (24, 20, 20),
    "M": (120, 60, 40),
    "T": (224, 83, 61),
    "P": (61, 90, 128),
    "K": (43, 43, 43),
}

_HEAD = [
    "....HHHHHHHHHHHHH....",
    "....HHHHHHHHHHHHH....",
    "...HHHHHHHHHHHHHHH...",
    "...HHSSSSSSSSSSSHH...",
    "...HHSSSSSSSSSSSHH...",
    "...HSSSSSSSSSSSSSH...",
    "...HSSSSSSSSSSSSSH...",
    "...HSSSSSSSSSSSSSH...",
    "...HSSEESSSSEESSSH...",
    "...HSSSSSMMSSSSSSH...",
    "...HHHSSSSSSSSSHHH...",
]

_LEGS = [
    "....PP.........PP....",
    "....PP.........PP....",
    "....PP.........PP....",
    "....PP.........PP....",
    "....KK.........KK....",
    "...KKK.........KKK...",
]

_TORSO = {
    FRAME_IDLE: [
        "....TTTTTTTTTTTTT....",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".SS.PPPPPPPPPPPPP.SS.",
    ],
    FRAME_RUN_A: [
        "....TTTTTTTTTTTTT....",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".SS.TTTTTTTTTTTTT.TT.",
        "....TTTTTTTTTTTTT.TT.",
        "....PPPPPPPPPPPPP.SS.",
    ],
    FRAME_RUN_B: [
        "....TTTTTTTTTTTTT....",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.TT.",
        ".TT.TTTTTTTTTTTTT.SS.",
        ".TT.TTTTTTTTTTTTT....",
        ".SS.PPPPPPPPPPPPP....",
    ],
}

_PIXEL_FRAMES = {
    frame: _HEAD + torso + _LEGS for frame, torso in _TORSO.items()
}


def build_sprite(frame=FRAME_IDLE, scale=2):
    pixels = _PIXEL_FRAMES[frame]
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
