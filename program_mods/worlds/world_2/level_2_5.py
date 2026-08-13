import pygame

# 2-5 "Cerberus": 6660px, first world boss arena. A single long open floor (no
# pits -- boss fights stay on flat ground) with walk-under dodge ledges every
# ~400-800px and two climbable 2-step towers. The checkpoint sits at x=1500,
# far from the right edge (5160px runway) so the post-last-world respawn cannot
# instantly re-trigger completion. Completion still means reaching the right
# edge until boss-defeat logic is implemented.

PLATFORMS = [
    # long open arena floor
    pygame.Rect(0, 700, 6660, 100),
    # dodge ledges (walk under, hop on for height)
    pygame.Rect(400, 620, 200, 26),
    pygame.Rect(1200, 620, 200, 26),
    pygame.Rect(3200, 620, 200, 26),
    pygame.Rect(4000, 620, 200, 26),
    pygame.Rect(4800, 620, 200, 26),
    pygame.Rect(6200, 620, 200, 26),
    # climbable towers (optional height advantage)
    pygame.Rect(2050, 620, 160, 26),  # tower 1
    pygame.Rect(2280, 560, 160, 26),
    pygame.Rect(2510, 500, 160, 26),
    pygame.Rect(5550, 620, 160, 26),  # tower 2
    pygame.Rect(5780, 560, 160, 26),
    pygame.Rect(6010, 500, 160, 26),
    # ceiling beams (decorative, above jump reach)
    pygame.Rect(300, 280, 400, 16),
    pygame.Rect(3000, 280, 400, 16),
    pygame.Rect(5200, 280, 400, 16),
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
