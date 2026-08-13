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
- **World transitions:** `_run_game` runs every level in sequence, then every
  world. A level completes when its checkpoint is activated AND the player
  reaches the right edge (`player.rect.left >= LEVEL_WIDTH`). Then:
  `fade_to_black` → `run_victory_scene` (placeholder, in
  `program_mods/victory/` — not implemented) → next level via
  `level.set_level(world_index, level_index)`, then `fade_from_black`. If the
  world has more levels, `level_index += 1`; else the next world (`world_index
  += 1`, `level_index = 0`). After the last world it loops to the last
  checkpoint instead of advancing. Fades are in `program_mods/game/fade.py`
  (`FADE_TIME` in `settings.py`). **Gotcha:** the `entering` flag for
  `fade_from_black` is initialized ONCE before the outer loop — never reset it
  at the top of the loop, or the fade-in becomes dead code (previous bug).
- **`set_level` caveat:** `program_mods/level/level.py` holds mutable module
  globals (`LEVEL_WIDTH`, `PLATFORMS`, …); `set_level(world_index,
  level_index)` rebinds them and the `level/__init__.py` re-syncs its
  re-exports. `backbone.py` reads through the `level` module object
  (`level.PLATFORMS`), NOT `from ..level import PLATFORMS` — a bare `import`
  would freeze world 1's data forever.
- Every package re-exports its public API via `__init__.py`
  (e.g. `from ..player import Player`); code consumes the package, not leaf modules.
- **Circular-import trap:** `start_screen` and `pause_menu` must be imported lazily
  inside `backbone()` / `_run_game()` (they transitively import `game`, which
  imports `backbone`). Any new package that imports from `program_mods.game` at
  module top level will break.
- Worlds = one package per world in `program_mods/worlds/world_<n>/`. Each world
  holds sub-levels: `world.py` defines a metadata dict
  `{"name": ..., "levels": (LEVEL_N_M, ...)}` importing one module per level
  (`level_1_1.py`, …), each defining
  `LEVEL_N_M = {"name", "width", "height", "spawn", "checkpoint", "platforms",
  "enemies", "items"}` (enemies/items are empty stubs for now). A level can add
  an optional `"decor"` key (see `program_mods/backdrop/`) that turns it into a
  room — wall, wainscot, window, door, lamp, rug, and furniture whose hitboxes
  match the visuals (solid pieces hop-over, thin pieces stay walk-under with an
  open gap) — plumbed as `level.DECOR`; only 1-1 uses it so far. Registered:
  `world_1/` (Captain's Quarters: 1-1 The Bedroom 2000px, 1-2 The Hallway
  ~1500px) and `world_2/` (Tutorial Deck: 2-1 Movement, 2-2 Melee & Parry, 2-3
  Aerial & Parry, 2-4 Mini-Boss, 2-5 Cerberus world boss 6660px).
  `world_3/`…`world_5/` are placeholder templates with `levels: ()` — NOT
  registered. Activate a world by giving it levels and appending its `WORLD_<n>`
  to `WORLDS` in `worlds/__init__.py`. `program_mods/level/level.py` exposes the
  active world/level (`WORLD`, `LEVEL`, `LEVEL_NAME`, `LEVEL_WIDTH`,
  `PLAYER_SPAWN`, `PLATFORMS`, …) and `set_level(world_index, level_index)`
  switches it at runtime (used by transitions). **Gotcha:** the last world's
  checkpoint must sit far from the right edge — a checkpoint near the edge
  re-triggers completion the moment the post-last-world respawn lands (previous
  bug).
- `program_mods/bank.py` and `system_mods/` (`eraser.py`, `oopsie.py`) are
  incomplete user scaffolding — leave alone.
- `program_mods/victory/` is an empty placeholder (`run_victory_scene`) for the
  post-world banner scene — implement it, don't delete it.
- `program_mods/hud/draw_hud()` renders the "world-level name" label in the top
  corner; it reads through the `level` module object (same set_level caveat as
  `backbone.py`), so it stays correct across transitions.

## Gotchas (verified in this build)

- **`pygame.font` is broken** here (circular import with `pygame.sysfont`). Always
  render text via `make_font(size)` from `program_mods/game/font.py` (falls back to
  `pygame._freetype`). Never `import pygame.font` directly.
- **`pygame.image.save` PNG fails** (`NotImplementedError: extended format`). Save
  BMP, convert with ffmpeg.
- AVX2 startup warning is cosmetic — ignore.
- Escape key = pause (not quit) once in-game.
