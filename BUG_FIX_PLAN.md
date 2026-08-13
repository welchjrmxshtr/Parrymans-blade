# Bug-Fix Planner — World Transitions

Live handoff for the next chat. Read `PROJECT_REVIEW.md` first; this file only adds
what's needed to fix the world-transition bugs found while testing.

Status: both bugs below are **confirmed** via headless reproduction
(`SDL_VIDEODRIVER=dummy`), none fixed yet. All world-transition work is still
**uncommitted** in the working tree.

---

## Bug 1 (CRITICAL) — `fade_from_black` never runs; game freezes on black screen

### Symptom
After completing a world, the screen fades to black and **never fades back in**.
The game is not hung (the player keeps running invisibly), but the player never sees
the world again. First completion looks like a hard freeze.

### Root cause
`program_mods/game/backbone.py:124` sets `entering = True` then `break`s out of the
inner loop. The **outer** loop immediately resets `entering = False` at
`backbone.py:54` before the inner loop's `if entering:` check at `backbone.py:112`
ever sees it. So `fade_from_black` is dead code in every transition path.

The fade counter (headless instrumentation) shows only `FADE_TO_BLACK`, never
`FADE_FROM_BLACK`:
```
  FADE_TO_BLACK #1 at t=2.31      (world 1 completed)
  FADE_TO_BLACK #2 at t=4.69      (world 1 re-completed after checkpoint loop)
  ...zero FADE_FROM_BLACK calls...
```

### Fix (proposed)
Initialize `entering = False` **once** before the outer `while True` loop (near
`backbone.py:40`), and delete the `entering = False` reset at `backbone.py:54`.
The existing `if entering:` block at `backbone.py:112-114` already sets
`entering = False` after running, so the flag survives the transition's `break` and
gets consumed on the first frame of the next world. Verify with the 2-fake-world
repro: expect `FADE_FROM_BLACK` after each `FADE_TO_BLACK`.

---

## Bug 2 (DESIGN / GAMEPLAY) — final-world checkpoint loop instantly re-completes

### Symptom
After the **last** world, the "loop to last checkpoint" behavior respawns the player
at the checkpoint, which sits near the right edge, so `player.rect.left >= LEVEL_WIDTH`
re-triggers completion almost immediately → infinite fade→respawn→fade cycle. With
Bug 1 present this is invisible (black screen); once Bug 1 is fixed this will show as
a visible stutter-loop where the world finishes ~0.3s after respawn.

### Evidence
`world_1/` checkpoint is at `(2310, 660)`, `LEVEL_WIDTH = 2400` → only **90px** from
the right edge. At `MOVE_SPEED = 300` that's ~0.3s from respawn to re-completion.
Headless repro (1 fake world, checkpoint at x=700 / width 800): player re-triggers
completion every ~2.3s of the fade loop.

Also note: `backbone.py:49` calls `checkpoint.activate()` on the loop respawn, and the
respawn point **is** the checkpoint rect, so line 88 would re-activate it anyway.

### Fix options (pick one — needs user decision)
- **A. One-shot completion per world:** set a `completed` flag when the transition
  fires; ignore the `checkpoint.activated and rect.left >= LEVEL_WIDTH` check while
  set. Clears on death respawn / restart. Keeps the "free-play the final world" intent.
- **B. Don't re-activate on loop:** remove `checkpoint.activate()` in the respawn
  branch and move the respawn point a little left of the checkpoint so the player must
  walk back onto it to re-arm completion. Restores meaning, but checkpoint near the
  edge still means a short walk to re-complete.
- **C. Accept + rely on real checkpoints:** only a fake-world artifact; real checkpoints
  should be placed away from the right edge. Requires no code change but leaves a trap
  for future world authors.

Recommended: **A** (simplest, matches "loop to the last checkpoint so the player can
keep playing" without the constant victory loop).

---

## Repro scripts (in `/tmp/opencode/`, not committed)
- `repro_loop.py` — headless single-fake-world run with a per-frame spy on
  `Player.update` and wrappers on `fade_to_black` / `fade_from_black`. Confirms Bug 1
  (no `FADE_FROM_BLACK`) and Bug 2 (repeat `FADE_TO_BLACK`). Watchdog posts QUIT.
- 2-fake-world variant (inline `python -c`) confirms the same on a normal world
  advance, not just the last-world path.

Run with:
`SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy .venv/bin/python /tmp/opencode/repro_loop.py`

---

## Verification checklist for the fix
1. `.venv/bin/python -m compileall -q program_mods main.py` — clean.
2. Headless repro: exactly one `FADE_TO_BLACK` then exactly one `FADE_FROM_BLACK` per
   world completion; no repeat completions inside one world (Bug 2 if option A).
3. Boot check still passes:
   `SDL_VIDEODRIVER=dummy SDL_AUDIODRIVER=dummy timeout 4 .venv/bin/python main.py`
   → exit code 124.
4. Real-world smoke test on a display (not SSH): complete world 1, see fade to black →
   victory placeholder → fade back in → world 2 spawn.
