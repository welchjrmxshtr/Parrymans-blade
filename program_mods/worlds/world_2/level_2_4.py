import pygame

# 2-4 "Mini-Boss": 3200px, tutorial mini-boss arena. Checkpoint sits before the
# fight so a respawn restarts the boss encounter, not the whole level.

PLATFORMS = [
    pygame.Rect(0, 700, 3200, 100),
    pygame.Rect(600, 620, 180, 26),
    pygame.Rect(1200, 540, 180, 26),
    pygame.Rect(1800, 620, 180, 26),
    pygame.Rect(2400, 540, 180, 26),
    pygame.Rect(2800, 640, 180, 26),
]

LEVEL_2_4 = {
    "name": "Mini-Boss",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (1000, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
