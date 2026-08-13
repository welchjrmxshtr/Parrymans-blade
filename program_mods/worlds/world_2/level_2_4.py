import pygame

# 2-4 "Mini-Boss": 3200px. One open arena floor -- no pits, so the mini-boss
# fight is never cheapened by an accidental fall. A mirrored pair of 2-step
# towers plus a center platform are all walk-under dodge routes; climbing them
# is optional. Checkpoint sits past the towers, before the exit runway.

PLATFORMS = [
    # open arena floor
    pygame.Rect(0, 700, 3200, 100),
    # left tower (walk under, climb to dodge)
    pygame.Rect(600, 620, 160, 26),
    pygame.Rect(820, 560, 140, 26),
    pygame.Rect(1060, 500, 140, 26),
    # right tower (mirrored)
    pygame.Rect(2000, 620, 160, 26),
    pygame.Rect(2220, 560, 140, 26),
    pygame.Rect(2440, 500, 140, 26),
    # center low platform
    pygame.Rect(1500, 600, 160, 26),
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(300, 280, 400, 16),
    pygame.Rect(2500, 280, 400, 16),
]

LEVEL_2_4 = {
    "name": "Mini-Boss",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2800, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
