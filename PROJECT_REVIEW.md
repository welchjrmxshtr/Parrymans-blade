# Parryman's Blade — Project Review & Continuation Guide

Handoff document for resuming work in a new agent window.

## What this is

A minimal 2D platformer built with **pygame 2.6.1** in Python 3.14. Set in "the
underworld" (per the README). You play a floating Grim Reaper navigating ship
deck platforms to a checkpoint. Two registered worlds, each made of sub-levels
(world 1: two levels; world 2: five tutorial levels + Cerberus boss).

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
│   ├── __init__.py          #   re-exports level.py constants + set_level() (re-syncs)
│   └── level.py             #   loads the ACTIVE world/level from worlds/; set_level(w,i)
├── worlds/
│   ├── world_1/             #   Captain's Quarters: 1-1 The Bedroom (2000px), 1-2 Hallway
│   │   ├── world.py         #     WORLD_1 = {"name", "levels": (LEVEL_1_1, LEVEL_1_2)}
│   │   ├── level_1_1.py     #     LEVEL_1_1 dict (name/width/height/spawn/checkpoint/…)
│   │   ├── level_1_2.py     #     LEVEL_1_2 dict
│   │   └── __init__.py      #     re-exports WORLD_1 + levels
│   ├── world_2/             #   Tutorial Deck: 2-1 Movement … 2-5 Cerberus (6660px)
│   │   ├── world.py         #     WORLD_2 = {"name", "levels": (LEVEL_2_1, … LEVEL_2_5)}
│   │   ├── level_2_1.py … level_2_5.py
│   │   └── __init__.py
│   ├── world_3/ … world_5/  #   placeholder templates (levels: (), NOT registered)
│   └── __init__.py          #   WORLDS registry (activate a world here)
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

`_run_game()` runs every level in sequence, then every world. A level completes
when its checkpoint is activated **and** the player reaches the right edge
(`player.rect.left >= LEVEL_WIDTH`). On completion: `fade_to_black` (2s) →
`run_victory_scene` (placeholder, not implemented) → next level via
`level.set_level(world_index, level_index)` (if the world has more levels,
`level_index += 1`; else next world, `level_index = 0`) → `fade_from_black`.
After the last world, the player loops to the last checkpoint (respawn there)
instead of advancing. **Gotcha:** `level.set_level()` rebinds module globals in
`level.py` and `level/__init__.py` re-syncs its re-exports; `backbone.py` must
read level data through the `level` module object (`level.PLATFORMS`), not
`from ..level import PLATFORMS` — a bare import would freeze world 1's data
forever. **Fade gotcha:** the `entering` flag for `fade_from_black` is
initialized once before the outer loop — never reset it at the top of the loop
or the fade-in becomes dead code (fixed bug; verified via headless transition
test in `/tmp/opencode/test_transitions.py`).

### Level data & "worlds" (how to add levels later)

Each world is one package in `program_mods/worlds/world_<n>/`. Each world
contains sub-levels: `world.py` holds a metadata dict with a `"levels"` tuple
of per-level dicts, one module per level:

```python
# world.py
from .level_1_1 import LEVEL_1_1
from .level_1_2 import LEVEL_1_2

WORLD_1 = {
    "name": "The Captain's Quarters",
    "levels": (LEVEL_1_1, LEVEL_1_2),
}
```

```python
# level_1_1.py
import pygame
PLATFORMS = [pygame.Rect(0, 700, 2000, 100), ...]
LEVEL_1_1 = {
    "name": "The Bedroom",
    "width": 2000, "height": 800,
    "spawn": (150, 500),
    "checkpoint": (1680, 640),
    "platforms": PLATFORMS,
    "enemies": [],   # empty stubs for now
    "items": [],     # 1-1's small inventory chest is planned, not implemented
}
```

Activate a world by giving it levels and appending its `WORLD_<n>` to the
`WORLDS` tuple in `worlds/__init__.py` (`world_3`…`world_5` are placeholder
templates with `levels: ()`, not registered). `level/level.py` picks the active
one (`WORLDS[0]`) and exposes `WORLD`, `LEVEL`, `LEVEL_NAME`, `LEVEL_WIDTH`,
`LEVEL_HEIGHT`, `PLAYER_SPAWN`, `CHECKPOINT_POS`, `PLATFORMS`, `ENEMIES`,
`ITEMS` — the rest of the game only talks to `program_mods.level`.
`level.set_level(world_index, level_index)` rebinds those globals at runtime
(used by transitions). **Gotcha:** the last world's checkpoint must sit far from
the right edge — a checkpoint near the edge re-triggers completion the moment the
post-last-world respawn lands (2-5 Cerberus uses x=1500 / width 6660).

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
- **Room decor** (`backdrop/build_decor.py`): `build_decor(width, height,
  platforms, spec)` returns one static world-size surface (or None) painting the
  back wall (wallpaper + wainscot + chair rail + baseboard), a window, picture
  frames, a door, a floor lamp and a rug, plus every piece listed in
  `spec["furniture"]` (keyed by platform rect, e.g. "bed", "wardrobe",
  "chest"). Solid furniture (platform height > 30) is painted as a complete
  piece (top face marks the landing surface) and backbone skips its plank-deck
  blit; thin furniture gets a body ending at the standing-head line + legs with
  an open walk-under gap. Levels opt in via `LEVEL["decor"]`, plumbed as
  `level.DECOR`; absent → no decor (all other levels unchanged).
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
 - **Levels** (`worlds/world_1/`, `worlds/world_2/`): height 800, ground @
   y=700; level heights vary. All 7 levels are **AI-verified playable** with the
   real player physics via `/tmp/opencode/test_levels_ai.py`
   (`PYTHONPATH=<repo> .venv/bin/python /tmp/opencode/test_levels_ai.py` →
   `ALL_LEVELS_CLEARABLE`). Design rules baked in: optional hops ≤80 px (max
   jump ≈112 px), forced gaps ≤180 px (max horizontal ≈240 px), walk-under
   clearances and, critically, no low platform (bottom < 660) may overhang a
   pit's run-up or jump trigger window (it bonks the jump — hit this twice in
   2-1). Layouts: 1-1 Bedroom 2000px (renders as an actual bedroom via the
   backdrop package -- wallpaper + wainscot wall, window above the bed, picture
   frames, door, floor lamp, rug. Hitboxes match the furniture: the LOW pieces
   footstool/crates/wardrobe/chest are solid to the floor (hop over them, 80px)
   while the TALL pieces bed/nightstand/desk/loft stay thin so the ground path
   walks UNDER them (decor draws body + legs with an open gap); optional
   forward-climbable loft chain footstool→bed→nightstand→desk→loft, two
   floorboard pits split by a mid-floor island at 1100–1240/1450–1600,
   checkpoint on the chest at (1885,620)), 1-2
   Hallway 1500px (door
   sills, trapdoor pit 700–860, crate stacks), 2-1 Movement 3200px (progressive
   pits 140/180/180 + hop steps), 2-2 Melee & Parry 3200px (4 flat encounter
   cells split by pits, low barrier, ledges), 2-3 Aerial & Parry 3200px
   (60 px-rise aerial chain over a void, practice ledge), 2-4 Mini-Boss 3200px
   (twin towers, center platform), 2-5 Cerberus 6660px (dodge ledges + towers,
   checkpoint at x=1500 far from the edge). 1-2's doors and 1-1's inventory
   chest are decorations/planned (no door or item system yet).

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
   `player/player.py`, `player/sprite.py`. Latest (this session): sub-level
   restructure — worlds hold `levels:` tuples (`worlds/world_1/` = 2 levels,
   `worlds/world_2/` = 5 levels), `set_world` → `set_level(world_index,
   level_index)`, `_run_game` advances level-first, the `fade_from_black`
   dead-code bug was fixed (see `BUG_FIX_PLAN.md`), and all levels were
   redesigned (thematic furniture/pits/aerial chain/boss arena) and verified by
   the headless AI playthrough (`test_levels_ai.py`: 7/7 `ALL_LEVELS_CLEARABLE`,
   transitions `TRANSITIONS_OK`).
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
- **More worlds** — the `worlds/` registry is ready; `world_3/`…`world_5/` are
  placeholder templates (`levels: ()`). Give a world sub-levels (one
  `level_<n>_<m>.py` per level) and register it in `worlds/__init__.py`; it
  automatically becomes reachable via the transition loop.
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
starve the pause menu's own `get()`). The full level→level → world→world →
last-world-loop transition walk is `/tmp/opencode/test_transitions.py`
(patches backbone's import-time globals: `Checkpoint`, `handle_events`,
`fade_to_black`/`fade_from_black`, and `Player.update` to auto-complete each
level; asserts the completion sequence and that `fade_from_black` runs after
every transition).
