import pygame

# 1-1 "The Bedroom": 2000px, small bedroom with a small inventory chest.
# The chest (items) is planned, not implemented yet -- ITEMS stays empty.

PLATFORMS = [
    pygame.Rect(0, 700, 2000, 100),
    pygame.Rect(220, 640, 160, 26),
    pygame.Rect(450, 580, 180, 26),
    pygame.Rect(700, 640, 140, 26),
    pygame.Rect(920, 560, 180, 26),
    pygame.Rect(1180, 640, 140, 26),
    pygame.Rect(1400, 560, 180, 26),
    pygame.Rect(1650, 640, 180, 26),
]

LEVEL_1_1 = {
    "name": "The Bedroom",
    "width": 2000,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (1680, 640),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
