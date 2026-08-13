import pygame

# 2-2 "Melee & Parry": 3200px. Four flat "encounter cells" for future enemy
# waves, separated by 140-160px pits. Cell 1 has a low barrier to hop. One
# optional ledge per cell gives height advantage for later melee/parry fights.
# Cells stay flat so melee is fought on level ground.

PLATFORMS = [
    # floor segments (pits: 800-940, 1600-1760, 2500-2660)
    pygame.Rect(0, 700, 800, 100),
    pygame.Rect(940, 700, 660, 100),
    pygame.Rect(1760, 700, 740, 100),
    pygame.Rect(2660, 700, 540, 100),
    # low barrier in cell 1 (hop over, 50px tall)
    pygame.Rect(480, 650, 20, 50),
    # optional ledges (walk under, hop on)
    pygame.Rect(1150, 620, 160, 26),  # cell 2
    pygame.Rect(1900, 620, 160, 26),  # cell 3
    pygame.Rect(2150, 560, 160, 26),  # cell 3 high ledge
    pygame.Rect(2750, 620, 160, 26),  # cell 4
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(1200, 280, 200, 16),
    pygame.Rect(2600, 280, 200, 16),
]

LEVEL_2_2 = {
    "name": "Melee & Parry",
    "width": 3200,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2950, 700),
    "platforms": PLATFORMS,
    "enemies": [],
    "items": [],
}
