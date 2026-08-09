import pygame

FRAME_IDLE = 0
FRAME_RUN_A = 1
FRAME_RUN_B = 2

_PALETTE = {
    "H": (48, 46, 68),
    "K": (20, 20, 32),
    "W": (230, 226, 218),
    "D": (12, 12, 18),
    "R": (58, 56, 82),
    "L": (84, 82, 112),
}

_HEAD = [
    ".....HHHHHHHHHHH.....",
    "...HHHHHHHHHHHHHHH...",
    "..HHHHHHHHHHHHHHHHH..",
    ".HHHHHHHHHHHHHHHHHHH.",
    ".HHHHHHHHHHHHHHHHHHH.",
    ".HHHKKKKKKKKKKKKKHHH.",
    ".HHHKKKWWWWWWWKKKHHH.",
    ".HHHKKKWDDWDDWKKKHHH.",
    ".HHHKKKWWWDWWWKKKHHH.",
    ".HHHKKKWDDDDDWKKKHHH.",
    ".HHHHHHHHHHHHHHHHHHH.",
]

_ROBE = [
    ".RRRRRRRRRRRRRRRRRRR.",
    "..RRRRRRRRLRRRRRRRR..",
    "...RRRRRRRLRRRRRRR...",
    "....RRRRRRLRRRRRR....",
    "....RRRRRRLRRRRRR....",
    ".....RRRRRLRRRRR.....",
    ".....RRRRL.RRRR......",
]

_TAIL = {
    FRAME_IDLE: [
        ".......RRRRRRR.......",
        "......RRRRRRRRR......",
        ".....RRRRRRRRRRR.....",
        ".....RRRRRRRRRRRR....",
        "....RRRRRRRRRRRRRR...",
        "....RRRR.RRRRRR.RR...",
        "...RRR..RRRRRR...R...",
    ],
    FRAME_RUN_A: [
        "......RRRRRRRRR......",
        ".....RRRRRRRRRRR.....",
        "....RRRRRRRRRRRRR....",
        "...RRRRRRRRRRRRRRR...",
        "..RRRRRRRRRRRRRRRRR..",
        "..RRRRRRRRRRRRR.RR...",
        ".RRRRRRRRRRR.RRRR....",
    ],
    FRAME_RUN_B: [
        ".......RRRRRRRRR.....",
        ".......RRRRRRRRRRR...",
        ".......RRRRRRRRRRRRR.",
        "......RRRRRRRRRRRRRRR",
        ".....RRRRRRRRRRRRRRRR",
        ".....RRRRRRRRRRRR.RRR",
        "......RRRRRRRR...RRRR",
    ],
}

_BOB = {FRAME_IDLE: 0, FRAME_RUN_A: -1, FRAME_RUN_B: 1}

_PIXEL_FRAMES = {
    frame: _HEAD + _ROBE + _TAIL[frame] for frame in _TAIL
}


def build_sprite(frame=FRAME_IDLE, scale=2):
    pixels = _PIXEL_FRAMES[frame]
    h = len(pixels)
    w = len(pixels[0])
    surf = pygame.Surface((w * scale, h * scale), pygame.SRCALPHA)
    bob = _BOB[frame] * scale
    for row, line in enumerate(pixels):
        for col, ch in enumerate(line):
            color = _PALETTE.get(ch)
            if color is None:
                continue
            pygame.draw.rect(surf, color, (col * scale, row * scale + bob, scale, scale))
    return surf
