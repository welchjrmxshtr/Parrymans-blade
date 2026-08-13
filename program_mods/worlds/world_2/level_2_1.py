import pygame

# 2-1 "Movement": 3200px, short movement tutorial (run + jump over low steps).

PLATFORMS = [
    pygame.Rect(0, 700, 3200, 100),
    pygame.Rect(300, 640, 200, 26),
    pygame.Rect(600, 580, 200, 26),
    pygame.Rect(900, 640, 200, 26),
    pygame.Rect(1200, 580, 200, 26),
    pygame.Rect(1500, 640, 200, 26),
    pygame.Rect(1800, 580, 200, 26),
    pygame.Rect(2100, 640, 200, 26),
    pygame.Rect(2400, 580, 200, 26),
    pygame.Rect(2700, 640, 200, 26),
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
