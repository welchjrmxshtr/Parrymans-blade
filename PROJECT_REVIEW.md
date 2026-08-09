# Parryman's Blade — Project Review & Continuation Guide

Handoff document for resuming work in a new agent window.

## What this is

A minimal 2D platformer built with **pygame 2.6.1** in Python 3.14. Set in "the
underworld" (per the README). Single level, player character, one checkpoint.

## Running the game

```bash
.venv/bin/python main.py        # play (needs a display; not over SSH)
```

- A/D or arrows: move · Space/W/Up: jump (short-hop on release) · Esc: quit
- Controls live in `program_mods/game/input.py`.

**Headless testing** (no display available):
```bash
SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 4 .venv/bin/python main.py
```
Exit code 124 (timeout killed it) = game ran without crashing.

The `.venv` is machine-specific. To move the project: copy everything **except
`.venv/` and `__pycache__/`**, then `python3 -m venv .venv &&
.venv/bin/pip install -r requirements.txt` (pygame==2.6.1).

## Architecture

Entry point `main.py` → `program_mods/game/backbone.py` (`backbone()` is the
game loop). Convention from the user: functions live in individual `.py` files;
each game element owns its own package under `program_mods/`.

```
main.py                      # launcher only
program_mods/
├── game/                    # orchestration
│   ├── backbone.py          #   main loop: update + render + checkpoint/respawn
│   ├── input.py             #   handle_events(), get_movement(keys)
│   ├── settings.py          #   window, FPS, colors, message text/timing
│   └── font.py              #   make_font(): pygame.font with _freetype fallback
├── player/
│   ├── player.py            #   Player: physics, collisions, run animation
│   └── sprite.py            #   pixel-art frames (idle, run A/B), palette
├── camera/
│   └── camera.py            #   follow + clamp to world, apply() for rendering
├── level/
│   └── level.py             #   world size, spawn, checkpoint pos, platform rects
├── checkpoint/
│   ├── checkpoint.py        #   Checkpoint: activation, collision
│   └── sprite.py            #   flag sprite (inactive gray / active green)
├── __init__.py
└── bank.py                  # EMPTY stub (user scaffolding — leave alone)
system_mods/                 # eraser.py, oopsie.py EMPTY stubs — leave alone
```

All packages re-export public API via `__init__.py` (e.g.
`from program_mods.player import Player`).

### Key mechanics

- **Player** (`player/player.py`): axis-separated AABB collision (move x →
  resolve → move y → resolve). Coyote time (0.1s), jump buffering (0.12s),
  variable jump height (cut `vy` on release). Grounding is stabilized by a
  platform-top check (`player.py:91`) — this fixed a bug where `on_ground`
  flickered every frame and broke the run animation. Run animation alternates
  `FRAME_RUN_A/B` every `RUN_FRAME_TIME` (0.12s) only while moving AND on
  ground; otherwise `FRAME_IDLE`. Sprite is 42×46 (21×23 px @ 2×).
- **Camera** (`camera/camera.py`): centers on player, clamps to world bounds
  (2400×800). Rendering uses `camera.apply(rect)` → screen-space rect.
- **Checkpoint** (`checkpoint/checkpoint.py`): 26×56 flag. On first collision,
  activates (flag turns green) and updates the respawn `spawn` point. Falling
  below `LEVEL_HEIGHT + 100` respawns the player at the current spawn.
- **Level** (`level/level.py`): ground spans 0–2400 @ y=700; 8 floating
  platforms (steps ascending to the right). Checkpoint sits on the final
  platform at (2310, 660). Max jump ≈108 px; platform steps are 60 px.

## Git state

- Repo: `https://github.com/welchjrmxshtr/Parrymans-blade.git` (branch `main`,
  tracks `origin/main`). Repo-local identity: `welchjrmxshtr /
  brahstudiodev@gmail.com`.
- Commits: `d670de3` `:init`, `ec5bb81` `0.0.1`, `45e5bed` merge of remote
  README/.gitignore.
- **UNCOMMITTED (do not lose):** the whole checkpoint feature
  (`program_mods/checkpoint/`), `program_mods/game/font.py`, plus edits to
  `game/backbone.py`, `game/settings.py`, `level/__init__.py`, `level/level.py`,
  `player/player.py`, `player/sprite.py` (arms run animation + grounding fix).
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

- **Legs animation** to match the arm swing (natural follow-up; makes running
  look complete).
- **Goal / win screen** — currently you can walk off the map edge and just
  respawn at the checkpoint. A flag-touch win state or map-end wall is a gap.
- **Enemies / hazards**, coins/collectibles, sound, tilemap loading.
- The user's earlier request was checkpoint "at the end of the map" — it was
  placed on top of the final platform (the ground path is blocked by that
  platform's side, so it doubles as a small jump challenge).

## Verification patterns used so far

Physics/animation/level logic is verified by short `python -c` scripts (no
pytest or test files exist yet) that run the real classes headless and assert on
positions/state, plus pixel-sampling sprite surfaces at expected coordinates.
