from ..worlds import WORLDS

WORLD_INDEX = 0
LEVEL_INDEX = 0
WORLD = WORLDS[WORLD_INDEX]
LEVEL = WORLD["levels"][LEVEL_INDEX]

LEVEL_NAME = LEVEL["name"]
LEVEL_WIDTH = LEVEL["width"]
LEVEL_HEIGHT = LEVEL["height"]
PLAYER_SPAWN = LEVEL["spawn"]
CHECKPOINT_POS = LEVEL["checkpoint"]
PLATFORMS = LEVEL["platforms"]
ENEMIES = LEVEL["enemies"]
ITEMS = LEVEL["items"]
DECOR = LEVEL.get("decor", None)


def set_level(world_index, level_index):
    global WORLD_INDEX, LEVEL_INDEX, WORLD, LEVEL, LEVEL_NAME, LEVEL_WIDTH, LEVEL_HEIGHT, PLAYER_SPAWN, CHECKPOINT_POS, PLATFORMS, ENEMIES, ITEMS, DECOR
    WORLD_INDEX = world_index
    LEVEL_INDEX = level_index
    WORLD = WORLDS[WORLD_INDEX]
    LEVEL = WORLD["levels"][LEVEL_INDEX]
    LEVEL_NAME = LEVEL["name"]
    LEVEL_WIDTH = LEVEL["width"]
    LEVEL_HEIGHT = LEVEL["height"]
    PLAYER_SPAWN = LEVEL["spawn"]
    CHECKPOINT_POS = LEVEL["checkpoint"]
    PLATFORMS = LEVEL["platforms"]
    ENEMIES = LEVEL["enemies"]
    ITEMS = LEVEL["items"]
    DECOR = LEVEL.get("decor", None)
