import pygame

# 1-2 "The Hallway": width scales with the project (~1500). Doors along the
# walls are decorations for now -- no door system yet.

PLATFORMS = [
    pygame.Rect(0, 700, 1500, 100),
    pygame.Rect(300, 640, 160, 26),
    pygame.Rect(700, 620, 180, 26),
    pygame.Rect(1100, 640, 160, 26),
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
