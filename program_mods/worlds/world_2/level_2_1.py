import pygame

# 2-1 "Movement": 3200px. Progressive tutorial -- three pits of growing width
# (140 / 180 / 180px, all directly jumpable at max range), optional hop steps
# in between, and a clear runway to the checkpoint. No near-max jumps
# forced: every optional step is 80px or less and walkable under.

PLATFORMS = [
    # floor segments (pits: 640-780, 1420-1600, 2280-2460)
    pygame.Rect(0, 700, 640, 100),
    pygame.Rect(780, 700, 640, 100),
    pygame.Rect(1600, 700, 680, 100),
    pygame.Rect(2460, 700, 740, 100),
    # optional hop steps
    pygame.Rect(260, 620, 180, 26),   # step A (80px)
    pygame.Rect(860, 620, 140, 26),   # low steps
    pygame.Rect(1080, 580, 140, 26),
    pygame.Rect(1300, 620, 60, 26),   # ends before pit 2's run-up (no head bonk)
    pygame.Rect(1680, 620, 180, 26),  # two-tier
    pygame.Rect(1940, 560, 180, 26),
    pygame.Rect(2160, 620, 50, 26),   # ends before pit 3's run-up (no head bonk)
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(1200, 280, 200, 16),
    pygame.Rect(2600, 280, 200, 16),
]

LEVEL_2_1 = {
    "name": "Movement",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2900, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
