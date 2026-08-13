import pygame

# 1-2 "The Hallway": ~1500px. Two low door sills to hop over (50px tall), then a
# trapdoor hole in the floor (700-860). Crate stacks against the far wall are an
# optional hop. Real doors/door system are planned, not implemented.

PLATFORMS = [
    # floor (trapdoor pit between 700 and 860)
    pygame.Rect(0, 700, 700, 100),
    pygame.Rect(860, 700, 640, 100),
    # low door sills to hop over
    pygame.Rect(180, 650, 20, 50),
    pygame.Rect(380, 650, 20, 50),
    # crate stacks (optional hop)
    pygame.Rect(1150, 620, 120, 26),
    pygame.Rect(1320, 560, 120, 26),
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(200, 280, 300, 16),
    pygame.Rect(1000, 280, 300, 16),
]

LEVEL_1_2 = {
    "name": "The Hallway",
    "width": 1500,
    "height": 800,
    "spawn": (100, 500),
    "checkpoint": (1300, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
