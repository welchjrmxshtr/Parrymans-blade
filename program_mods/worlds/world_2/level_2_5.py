import pygame

# 2-5 "Cerberus": 6660px, first world boss arena. Checkpoint is placed far from
# the right edge (x=1500) so a loop-back respawn is NOT instantly at the edge --
# this keeps the re-completion loop bug from triggering. Completion still means
# reaching the right edge until boss-defeat logic is implemented.

PLATFORMS = [
    pygame.Rect(0, 700, 6660, 100),
    pygame.Rect(800, 620, 200, 26),
    pygame.Rect(1500, 560, 200, 26),
    pygame.Rect(2400, 620, 200, 26),
    pygame.Rect(3300, 560, 200, 26),
    pygame.Rect(4200, 620, 200, 26),
    pygame.Rect(5100, 560, 200, 26),
    pygame.Rect(5900, 640, 200, 26),
]

LEVEL_2_5 = {
    "name": "Cerberus",
    "width": 6660,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (1500, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
