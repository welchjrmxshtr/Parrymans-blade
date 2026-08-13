import pygame

# 2-3 "Aerial & Parry": 3200px, aerial attack parry tutorial (more vertical).

PLATFORMS = [
    pygame.Rect(0, 700, 3200, 100),
    pygame.Rect(300, 640, 160, 26),
    pygame.Rect(550, 560, 160, 26),
    pygame.Rect(800, 480, 160, 26),
    pygame.Rect(1050, 560, 160, 26),
    pygame.Rect(1300, 640, 160, 26),
    pygame.Rect(1600, 560, 160, 26),
    pygame.Rect(1850, 480, 160, 26),
    pygame.Rect(2100, 560, 160, 26),
    pygame.Rect(2350, 640, 160, 26),
    pygame.Rect(2650, 560, 160, 26),
    pygame.Rect(2900, 640, 160, 26),
]

LEVEL_2_3 = {
    "name": "Aerial & Parry",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2950, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
