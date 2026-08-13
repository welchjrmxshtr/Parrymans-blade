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
    "S": (188, 192, 208),  # scythe blade (pale steel)
    "T": (84, 66, 50),     # scythe handle (dark wood)
    "V": (190, 36, 42),    # blood dripping off the blade
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

# The body is drawn BODY_TOP rows down so the scythe can rise above the head.
# One row per sprite row; the scythe strip sits to the RIGHT of the body.
BODY_TOP = 5

# Scythe rested over the shoulder: the blade arcs up past the head (top rows)
# with its hollow cradled toward the body, handle running down beside the robe.
# Drawn behind the body. Flipped as a whole when the player turns, so the blade
# keeps hanging toward the player in both facing directions.
_SCYTHE = [
    "....SS.....",   # blade tip over the shoulder
    "....SSS....",
    ".....SSS...",
    "......SSS..",
    ".......SSS.",
    "........SS.",
    ".........SS",
    ".........VS",   # blood on the blade's inner edge
    "........SS.",
    ".......VS..",   # blood running off the blade
    ".......V...",   # hanging drip
    "......V....",   # drip
    "......T....",   # handle begins
    "......T....",
    "......T....",
    "......T....",
    ".....T.....",
    ".....T.....",
    ".....T.....",
    ".....T.....",
    "....T......",
    "....T......",
    "....T......",
    "...TT......",
    "....TT.....",
]

# A single blood drop that falls beside the handle; shifts per frame so the
# float cycle reads as a slow drip.
_DRIPS = {
    FRAME_IDLE: [(12, 7)],
    FRAME_RUN_A: [(13, 7)],
    FRAME_RUN_B: [(14, 7)],
}

_PIXEL_FRAMES = {
    frame: _HEAD + _ROBE + _TAIL[frame] for frame in _TAIL
}


class _SpriteSurface(pygame.Surface):
    """Surface that knows how far its body sits below the top edge."""

    def __init__(self, size, *args, body_top=0, **kwargs):
        super().__init__(size, *args, **kwargs)
        self.body_top = body_top


def build_sprite(frame=FRAME_IDLE, scale=2):
    pixels = _PIXEL_FRAMES[frame]
    body_w = len(pixels[0])
    body_h = len(pixels)
    scythe_w = len(_SCYTHE[0])
    w = (body_w + scythe_w) * scale
    h = (BODY_TOP + body_h) * scale
    surf = _SpriteSurface((w, h), pygame.SRCALPHA, body_top=BODY_TOP * scale)
    bob = _BOB[frame] * scale
    # scythe first so the body draws over its handle (carried behind him)
    for row, line in enumerate(_SCYTHE):
        for col, ch in enumerate(line):
            color = _PALETTE.get(ch)
            if color is None:
                continue
            pygame.draw.rect(surf, color, ((body_w + col) * scale, row * scale + bob, scale, scale))
    for row, line in enumerate(pixels):
        for col, ch in enumerate(line):
            color = _PALETTE.get(ch)
            if color is None:
                continue
            pygame.draw.rect(surf, color, (col * scale, (row + BODY_TOP) * scale + bob, scale, scale))
    for row, col in _DRIPS[frame]:
        pygame.draw.rect(surf, _PALETTE["V"], ((body_w + col) * scale, row * scale + bob, scale, scale))
    return surf
