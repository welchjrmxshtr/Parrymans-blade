import pygame

# 2-3 "Aerial & Parry": 3200px. The core is an aerial corridor over the void
# (x=500-2000): a chain of 180px platforms stepping up 60px per hop to a 460px
# apex, then mirrored down to the landing floor. Missing a hop drops you out of
# the level. The landing zone is open ground with one optional practice ledge.

PLATFORMS = [
    # floor (spawn ledge + landing/end floor; void 500-2000 between them)
    pygame.Rect(0, 700, 500, 100),
    pygame.Rect(2000, 700, 1200, 100),
    # aerial chain (60px rises, 60px gaps, 180px wide)
    pygame.Rect(560, 640, 180, 26),   # step 1 (80px up from the spawn ledge)
    pygame.Rect(800, 580, 180, 26),
    pygame.Rect(1040, 520, 180, 26),
    pygame.Rect(1280, 460, 180, 26),  # apex
    pygame.Rect(1520, 460, 180, 26),
    pygame.Rect(1760, 520, 180, 26),  # descent
    pygame.Rect(2000, 580, 180, 26),
    pygame.Rect(2240, 640, 180, 26),
    # optional practice ledge on the landing floor (walk under, hop on)
    pygame.Rect(2300, 620, 160, 26),
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(900, 280, 400, 16),
    pygame.Rect(2600, 280, 200, 16),
]

LEVEL_2_3 = {
    "name": "Aerial & Parry",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2970, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
