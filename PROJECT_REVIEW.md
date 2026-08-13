# Parryman's Blade — Project Review & Continuation Guide

Handoff document for resuming work in a new agent window.

## What this is

A minimal 2D platformer built with **pygame 2.6.1** in Python 3.14. Set in "the
underworld" (per the README). You play a floating Grim Reaper navigating ship
deck platforms to a checkpoint. Single level (world 1), one checkpoint.

## Running the game

```bash
.venv/bin/python main.py        # play (needs a display; not over SSH)
```

- Start screen: ENTER/Space to start, ESC to quit.
- In game: A/D or arrows move · Space/W/Up jump (short-hop on release) · ESC
  pause.
- Pause menu (arrow keys/W/S to navigate, Enter to select, ESC to resume):
  Resume · Restart · Quit to Title · Quit to Desktop.
- Controls live in `program_mods/game/input.py` (movement/jump) and the pause
  trigger is checked in `backbone.py`.

**Headless testing** (no display available):
```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 4 .venv/bin/python main.py
```
Exit code 124 (timeout killed it) = game ran without crashing. Note: the game
blocks on the start screen until input; 4s timeout is enough to prove it boots.

The `.venv` is machine-specific. To move the project: copy everything **except
`.venv/` and `__pycache__/`**, then `python3 -m venv .venv &&
.venv/bin/pip install -r requirements.txt` (pygame==2.6.1).

## Architecture

Entry point `main.py` → `program_mods/game/backbone.py` (`backbone()` is the
entry; `_run_game()` is the game loop). Convention from the user: functions
live in individual `.py` files; each game element owns its own package under
`program_mods/`.

```
main.py                      # launcher only
program_mods/
├── game/                    # orchestration
│   ├── backbone.py          #   outer loop (title→game→title); _run_game() multi-world loop + transitions
│   ├── input.py             #   handle_events(), get_movement(keys)
│   ├── settings.py          #   window, FPS, colors, message text/timing, FADE_TIME
│   ├── font.py              #   make_font(): pygame.font with _freetype fallback
│   └── fade.py              #   fade_to_black() / fade_from_black() over FADE_TIME
├── player/
│   ├── player.py            #   Player: physics, collisions, float cycle, hover/shadow
│   └── sprite.py            #   reaper pixel frames (hood+skull, robe, swaying tail)
├── camera/
│   └── camera.py            #   follow + clamp to world, apply() for rendering
├── level/
│   ├── __init__.py          #   re-exports level.py constants + set_world() (re-syncs)
│   └── level.py             #   loads the ACTIVE world from worlds/; set_world(index)
├── worlds/
│   ├── world_1/              #   ACTIVE world (WORLDS[0]); one package per world
│   │   ├── world.py          #     metadata dict: name, size, spawn, checkpoint
│   │   ├── platforms.py      #     PLATFORMS: list of pygame.Rect
│   │   ├── enemies.py        #     ENEMIES (empty stub)
│   │   ├── items.py          #     ITEMS (empty stub)
│   │   └── __init__.py       #     re-exports WORLD_1 + data lists
│   ├── world_2/ … world_5/   #   placeholder templates (same layout, not registered)
│   └── __init__.py           #   WORLDS registry (activate a world here)
├── platform/
│   └── deck.py              #   build_deck(w,h): cached wooden ship-deck texture
├── checkpoint/
│   ├── checkpoint.py        #   Checkpoint: activation, collision
│   └── sprite.py            #   flag sprite (inactive gray / active green)
├── start_screen/
│   └── start_screen.py      #   run_start_screen(): title, mascot, ENTER to start
├── pause_menu/
│   └── pause_menu.py        #   run_pause_menu(): Resume/Restart/Title/Quit
├── victory/
│   └── victory.py           #   run_victory_scene(): PLACEHOLDER (not implemented)
├── __init__.py
└── bank.py                  # EMPTY stub (user scaffolding — leave alone)
system_mods/                 # eraser.py, oopsie.py EMPTY stubs — leave alone
```

All packages re-export public API via `__init__.py` (e.g.
`from program_mods.player import Player`). `start_screen` and `pause_menu` are
imported lazily inside `backbone.py` to avoid a circular import
(`start_screen → game → backbone → start_screen`).

### World transitions

`_run_game()` runs every world in sequence. A world completes when its checkpoint
is activated **and** the player reaches the right edge
(`player.rect.left >= LEVEL_WIDTH`). On completion: `fade_to_black` (2s) →
`run_victory_scene` (placeholder, not implemented) → next world via
`level.set_world(index)` → `fade_from_black`. After the last world, the player
loops to the last checkpoint (respawn there) instead of advancing, since only 5
world slots exist and more are planned. **Gotcha:** `level.set_world()` rebinds
module globals in `level.py` and `level/__init__.py` re-syncs its re-exports;
`backbone.py` must read world data through the `level` module object
(`level.PLATFORMS`), not `from ..level import PLATFORMS` — a bare import would
freeze world 1's data forever.

### Level data & "worlds" (how to add levels later)

Each world is one package in `program_mods/worlds/world_<n>/` with a shared
layout: `world.py` holds the metadata dict (name/size/spawn/checkpoint) plus
references to the data lists; `platforms.py` / `enemies.py` / `items.py` hold the
world-building data (enemies/items are empty stubs for now):

```python
# world.py
from .platforms import PLATFORMS
from .enemies import ENEMIES
from .items import ITEMS

WORLD_1 = {
    "name": "The Underdeck",
    "width": 2400, "height": 800,
    "spawn": (150, 500),
    "checkpoint": (2310, 660),
    "platforms": PLATFORMS,
    "enemies": ENEMIES,
    "items": ITEMS,
}
```

```python
# platforms.py
import pygame
PLATFORMS = [pygame.Rect(0, 700, 2400, 100), ...]
```

Activate a world by importing its package in `worlds/__init__.py` and appending
its `WORLD_<n>` to the `WORLDS` tuple (`world_2`…`world_5` are placeholder
templates, not yet registered). `level/level.py` picks the active one
(`WORLDS[0]`) and exposes `LEVEL_WIDTH`, `LEVEL_HEIGHT`, `PLAYER_SPAWN`,
`CHECKPOINT_POS`, `PLATFORMS`, `ENEMIES`, `ITEMS` — the rest of the game only
talks to `program_mods.level`. `level.set_world(index)` rebinds those globals at
runtime (used by world transitions).

### Key mechanics

- **Player** (`player/player.py`): axis-separated AABB collision (move x →
  resolve → move y → resolve). Coyote time (0.1s), jump buffering (0.12s),
  variable jump height (cut `vy` on release). Grounding is stabilized by a
  platform-top check (`player.py:91`).
- **Floating reaper** (`player/sprite.py` + `player.py`): the reaper no longer
  runs — a continuous float cycle (RUN_A → IDLE → RUN_B → IDLE, 0.2s/frame)
  bobs the whole sprite ±1px and sways a tattered robe tail left/right. The
  animation plays even while idle. `player.py` `draw()` renders the 42×50
  sprite 10px above the hitbox (`HOVER`) with a soft shadow beneath, so he
  appears to hover above the deck. Hitbox stays 42×46.
- **Camera** (`camera/camera.py`): centers on player, clamps to world bounds.
  Rendering uses `camera.apply(rect)` → screen-space rect.
- **Ship-deck platforms** (`platform/deck.py`): `build_deck(w, h)` procedurally
  draws alternating wood-tone planks with bevel, seam lines, staggered butt
  joints + nails, and a dark underside edge; results are cached per size.
  `backbone.py` pre-renders every platform's deck once and blits per frame.
- **Checkpoint** (`checkpoint/checkpoint.py`): 26×56 flag. On first collision,
  activates (flag turns green) and updates the respawn `spawn` point. Falling
  below `LEVEL_HEIGHT + 100` respawns at the current spawn. "Restart" from the
  pause menu resets player/camera/checkpoint and deactivates the flag.
- **Start screen** (`start_screen/start_screen.py`): title, floating reaper
  mascot (2×), blinking "Press ENTER", controls hint. Returns True to play,
  False to quit.
- **Pause menu** (`pause_menu/pause_menu.py`): frozen frame + dark overlay,
  keyboard-selectable items. Returns "resume" | "restart" | "title" | "quit".
  `backbone.py` outer loop sends "title" back to the start screen. `dt` is
  clamped to 1/20s so a long pause doesn't teleport the player on resume.
- **Level 1** (`worlds/world_1/`): ground spans 0–2400 @ y=700; 8 floating
  platforms (steps ascending to the right). Checkpoint on the final platform at
  (2310, 660). Max jump ≈108 px; platform steps are 60 px.

## Git state

- Repo: `https://github.com/welchjrmxshtr/Parrymans-blade.git` (branch `main`,
  tracks `origin/main`). Repo-local identity: `welchjrmxshtr /
  brahstudiodev@gmail.com`.
- Commits: `d670de3` `:init`, `ec5bb81` `0.0.1`, `45e5bed` merge of remote
  README/.gitignore, `ce549fc` checkpoint + run animation + review.
- **UNCOMMITTED (do not lose):** everything since `ce549fc` — Grim Reaper
  sprite redesign + floating/tail animation, hover + shadow, ship-deck platform
  textures (`program_mods/platform/`), start screen (`start_screen/`), pause
  menu (`pause_menu/`), worlds data structure (`worlds/`), plus edits to
  `backbone.py`, `input.py` (ESC = pause, not quit), `settings.py`, `level.py`,
  `player/player.py`, `player/sprite.py`.
- User commits only when explicitly asked.

## Known issues & environment quirks

1. **`pygame.font` is broken in this build** (circular import between
   `pygame/font.py` — the freetype shim — and `pygame/sysfont.py`). Font
   rendering falls back to `pygame._freetype` via `game/font.py`. Do not use
   `pygame.font` directly. On machines with a normal pygame, the fallback is
   skipped.
2. **`pygame.image.save(...)` PNG fails** (`NotImplementedError: saving images
   of extended format is not available`) on this locally-compiled pygame. Save
   BMP or convert with ffmpeg. (Also: `pygame.image.load` of PNGs is untested.)
3. **AVX2 warning** on startup ("pygame was not built with support for it") —
   cosmetic, ignore.
4. Building headless screenshots requires converting the dummy-display surface
   (save as BMP, convert with `ffmpeg -i x.bmp x.png`).

## Suggested next steps (not yet implemented)

- **Victory scene** — `program_mods/victory/run_victory_scene()` is a placeholder
  no-op; world transitions now call it after the fade-to-black, between the two
  fades. Implement the banner + short scene there.
- **More worlds** — the `worlds/` registry is ready; design `world_2/` (fill in
  its `world.py`/`platforms.py` and register it in `worlds/__init__.py`). Each
  new world automatically becomes reachable via the transition loop.
- **Enemies / hazards, coins/collectibles**, sound, tilemap loading.
- **Direction-aware tail** — the robe tail sways horizontally in-place; it
  could stream behind the reaper based on `facing`.
- Title/subtitle text on the start screen are placeholders ("REAPER'S DECK" /
  "A float through the underworld") — rename when the game gets a real name.

## Verification patterns used so far

Physics/animation/level logic is verified by short `python -c` scripts (no
pytest or test files exist yet) that run the real classes headless and assert on
positions/state, plus pixel-sampling sprite surfaces at expected coordinates.
`_run_game` end-to-end sequences (pause→resume→quit, pause→restart→title) are
driven by posting `pygame.event` KEYDOWNs from a daemon thread on staged delays
(because `pygame.event.get()` drains the queue, pre-posted events alone would
starve the pause menu's own `get()`).
