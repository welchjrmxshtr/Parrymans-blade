import pygame

# 1-1 "The Bedroom": 2000px. Reads as a room, not a platformer: the backdrop
# package paints the back wall (wallpaper, wainscot, window above the bed,
# picture frames, a door and a floor lamp) and a rug on the final floor.
# Hitboxes now match the furniture visuals: the LOW pieces (footstool, crates,
# wardrobe, inventory chest) are solid to the floor -- you hop over them (80px,
# well within the ~112px jump) -- while the TALL pieces (bed, nightstand, desk,
# loft shelf) stay thin so the ground path passes UNDER them (decor renders
# them with a body + legs and an open gap). The loft chain climbs footstool ->
# bed -> nightstand -> desk -> loft (80px then 60px hops, forward-climbable
# from spawn). The only forced hazards are two broken-floorboard pits split by
# a mid-floor island (1100-1240 and 1450-1600). The inventory chest (last
# platform) holds the checkpoint -- jump onto it or hop into the flag. The
# inventory system itself is planned, not implemented.

PLATFORMS = [
    # floor: two broken-floorboard pits with a mid-floor island between them
    pygame.Rect(0, 700, 1100, 100),      # main floor (0-1100)
    pygame.Rect(1240, 700, 210, 100),    # island (1240-1450)
    pygame.Rect(1600, 700, 400, 100),    # final floor (1600-2000)
    # solid furniture (hop over: 80px from the ground, tops all at y=620)
    pygame.Rect(240, 620, 140, 80),      # footstool (also starts the loft chain)
    pygame.Rect(1300, 620, 90, 80),      # crate stack on the island
    pygame.Rect(1700, 620, 120, 80),     # wardrobe
    pygame.Rect(1820, 620, 130, 80),     # inventory chest (checkpoint on top)
    # tall furniture chain (walk UNDER; hops 60px each)
    pygame.Rect(420, 560, 200, 24),      # bed (60px above the footstool)
    pygame.Rect(660, 500, 140, 24),      # nightstand (60px above the bed)
    pygame.Rect(840, 440, 140, 24),      # desk (60px above the nightstand)
    pygame.Rect(1020, 380, 70, 24),      # loft shelf (60px above the desk)
]

# Backdrop spec for the room decor. "furniture" rects mirror the platform
# hitboxes above. Solid pieces (height 80) are painted as complete furniture
# (top face + body); thin pieces are painted with a body + legs leaving an open
# walk-under gap. "loft" is a wall-mounted shelf (no floor contact).
DECOR = {
    "door": (20, 470, 100, 230),
    "window": (400, 330, 220, 150),
    "pictures": [
        (190, 360, 120, 90, "ship"),
        (700, 300, 120, 90, "portrait"),
    ],
    "lamp": (145, 545),
    "rug": (1640, 700, 180, 45),
    "furniture": {
        (240, 620, 140, 80): "stool",
        (420, 560, 200, 24): "bed",
        (660, 500, 140, 24): "nightstand",
        (840, 440, 140, 24): "desk",
        (1020, 380, 70, 24): "loft",
        (1300, 620, 90, 80): "crates",
        (1700, 620, 120, 80): "wardrobe",
        (1820, 620, 130, 80): "chest",
    },
}

LEVEL_1_1 = {
    "name": "The Bedroom",
    "width": 2000,
    "height": 800,
    "spawn": (150, 500),
    "checkpoint": (1885, 620),
    "platforms": PLATFORMS,
    "decor": DECOR,
    "enemies": [],
    "items": [],
}
