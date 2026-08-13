from . import level as _world_data
from .level import (
    WORLD, LEVEL, LEVEL_NAME, LEVEL_WIDTH, LEVEL_HEIGHT,
    PLAYER_SPAWN, CHECKPOINT_POS, PLATFORMS, ENEMIES, ITEMS, DECOR,
    WORLD_INDEX, LEVEL_INDEX, set_level,
)

_LEVEL_NAMES = (
    "WORLD", "LEVEL", "LEVEL_NAME", "LEVEL_WIDTH", "LEVEL_HEIGHT",
    "PLAYER_SPAWN", "CHECKPOINT_POS", "PLATFORMS", "ENEMIES", "ITEMS", "DECOR",
    "WORLD_INDEX", "LEVEL_INDEX",
)


def _sync():
    for name in _LEVEL_NAMES:
        globals()[name] = getattr(_world_data, name)


def set_level(world_index, level_index):
    _world_data.set_level(world_index, level_index)
    _sync()
