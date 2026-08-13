import pygame

# 2-2 "Melee & Parry": 3200px, melee parry tutorial.

PLATFORMS = [
    pygame.Rect(0, 700, 3200, 100),
    pygame.Rect(350, 640, 200, 26),
    pygame.Rect(700, 580, 200, 26),
    pygame.Rect(1050, 640, 200, 26),
    pygame.Rect(1400, 580, 200, 26),
    pygame.Rect(1750, 640, 200, 26),
    pygame.Rect(2100, 580, 200, 26),
    pygame.Rect(2450, 640, 200, 26),
    pygame.Rect(2800, 640, 200, 26),
]

LEVEL_2_2 = {
    "name": "Melee & Parry",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2900, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
