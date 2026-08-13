# AGENTS.md

2D pygame platformer ("Parryman's Blade"). Python 3.14.6, pygame==2.6.1 (pinned in
`requirements.txt`), local `.venv` (machine-specific, gitignored).

**Start here:** `PROJECT_REVIEW.md` is the live handoff doc — read it before major
work. This file only adds what the review doesn't make obvious.

## Run & verify

- Play (needs a display, not over SSH): `.venv/bin/python main.py`
- Headless boot check (exit code 124 = ran without crashing; the game blocks on the
  start screen until input):
  `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 4 .venv/bin/python main.py`
- No test suite, no linter/config of any kind. Verify logic with short `python -c`
  scripts that run the real classes headless (see PROJECT_REVIEW.md "Verification
  patterns"). Never `pip install` into `.venv` casually; pygame is the only dep.

## Architecture

User convention (stated in `main.py`): one function per `.py` file, functions live
in individual source files, each game element owns a package under `program_mods/`.

- Entry: `main.py` → `program_mods/game/backbone.py` (`backbone()` outer loop,
  `_run_game()` game loop).
- **World transitions:** `_run_game` runs every world in sequence. World completes
  when its checkpoint is activated AND the player reaches the right edge
  (`player.rect.left >= LEVEL_WIDTH`). Then: `fade_to_black` → `run_victory_scene`
  (placeholder, in `program_mods/victory/` — not implemented) → next world via
  `set_world(index)`, then `fade_from_black`. After the last world it loops to the
  last checkpoint instead of advancing. Fades are in `program_mods/game/fade.py`
  (`FADE_TIME` in `settings.py`).
- **`set_world` caveat:** `program_mods/level/level.py` holds mutable module globals
  (`LEVEL_WIDTH`, `PLATFORMS`, …); `set_world(index)` rebinds them and the
  `level/__init__.py` re-syncs its re-exports. `backbone.py` reads through the
  `level` module object (`level.PLATFORMS`), NOT `from ..level import PLATFORMS` —
  a bare `import` would freeze world 1's data forever.
- Every package re-exports its public API via `__init__.py`
  (e.g. `from ..player import Player`); code consumes the package, not leaf modules.
- **Circular-import trap:** `start_screen` and `pause_menu` must be imported lazily
  inside `backbone()` / `_run_game()` (they transitively import `game`, which
  imports `backbone`). Any new package that imports from `program_mods.game` at
  module top level will break.
- Worlds = one package per world in `program_mods/worlds/world_<n>/`: `world.py`
  (metadata dict: name/size/spawn/checkpoint), `platforms.py` (`PLATFORMS` rects),
  `enemies.py` / `items.py` (empty stubs for now). `world_1/` is active;
  `world_2/`…`world_5/` are placeholder templates. Activate a world by importing
  it in `worlds/__init__.py` and appending to the `WORLDS` tuple.
  `program_mods/level/level.py` picks `WORLDS[0]` and re-exports `PLATFORMS`,
  `ENEMIES`, `ITEMS`, `PLAYER_SPAWN`, etc. — the rest of the game talks only to
  `program_mods.level`. `set_world(index)` switches the active world at runtime
  (used by transitions).
- `program_mods/bank.py` and `system_mods/` (`eraser.py`, `oopsie.py`) are
  incomplete user scaffolding — leave alone.
- `program_mods/victory/` is an empty placeholder (`run_victory_scene`) for the
  post-world banner scene — implement it, don't delete it.

## Gotchas (verified in this build)

- **`pygame.font` is broken** here (circular import with `pygame.sysfont`). Always
  render text via `make_font(size)` from `program_mods/game/font.py` (falls back to
  `pygame._freetype`). Never `import pygame.font` directly.
- **`pygame.image.save` PNG fails** (`NotImplementedError: extended format`). Save
  BMP, convert with ffmpeg.
- AVX2 startup warning is cosmetic — ignore.
- Escape key = pause (not quit) once in-game.
