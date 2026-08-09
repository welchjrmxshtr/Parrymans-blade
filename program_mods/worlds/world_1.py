import pygame

WORLD_1 = {
    "name": "The Underdeck",
    "width": 2400,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2310, 660),
    "platforms": [
        pygame.Rect(0, 700, 2400, 100),
        pygame.Rect(260, 640, 160, 26),
        pygame.Rect(500, 580, 160, 26),
        pygame.Rect(740, 520, 180, 26),
        pygame.Rect(1020, 580, 160, 26),
        pygame.Rect(1260, 520, 180, 26),
        pygame.Rect(1520, 460, 200, 26),
        pygame.Rect(1860, 600, 180, 26),
        pygame.Rect(2130, 660, 270, 26),
    ],
}
