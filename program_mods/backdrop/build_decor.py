import pygame

# Room decor for a level. `build_decor` returns one static, full-world-size
# surface (or None when the level has no "decor" key) that paints the back wall
# and furniture bodies; backbone.py blits it between the platforms and the
# player. Levels opt in via LEVEL["decor"]:
#
#   {
#     "door":     (x, y, w, h),
#     "window":   (x, y, w, h),
#     "pictures": [(x, y, w, h, "ship" | "portrait"), ...],
#     "lamp":     (x, shade_top),
#     "rug":      (x, y, w, h),
#     "furniture": { (left, top, w, h): kind, ... },  # keyed by platform rect
#   }
#
# The "furniture" map mirrors the thin platform hitboxes: the deck surface drawn
# on top of them is the furniture's top, and the solid body + accents painted
# here make them read as furniture against the back wall. Bodies run to the
# floor; the player simply passes in front of them (decor blits before the
# player), so the walk-under hitboxes don't need to match the visuals.

FLOOR_Y = 700
HEAD_LINE = 654  # standing player's head height on the floor

WALL_BASE = (88, 98, 118)
WALL_ALT = (82, 92, 112)
WAIN_BASE = (108, 82, 54)
WAIN_LINE = (62, 45, 30)
RAIL = (146, 116, 80)
BASEBOARD = (40, 28, 18)
FRAME = (62, 45, 30)
BODY = (98, 74, 48)
BODY_DARK = (79, 59, 38)
LEG = (40, 28, 18)
GLASS = (24, 36, 64)
MOON = (214, 214, 196)
STAR = (220, 226, 240)
LIGHT = (200, 180, 140)
RUG = (96, 42, 48)
RUG_EDGE = (130, 62, 68)
PILLOW = (198, 190, 172)
BLANKET = (148, 68, 80)
PLANT_POT = (150, 110, 70)
PLANT = (74, 128, 84)
BOOKS = [(150, 60, 60), (70, 90, 150), (120, 100, 60), (90, 120, 90), (150, 120, 130)]


def build_decor(width, height, platforms, spec):
    if spec is None:
        return None
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    _paint_wall(surf, width)
    _paint_door(surf, spec.get("door"))
    _paint_window(surf, spec.get("window"))
    for x, y, w, h, kind in spec.get("pictures", []):
        _paint_picture(surf, pygame.Rect(x, y, w, h), kind)
    _paint_lamp(surf, spec.get("lamp"))
    _paint_rug(surf, spec.get("rug"))
    kinds = spec.get("furniture", {})
    for plat in platforms:
        key = (plat.left, plat.top, plat.width, plat.height)
        kind = kinds.get(key)
        if kind is None:
            continue
        _paint_furniture(surf, plat, kind)
    return surf


def _paint_wall(surf, width):
    floor = FLOOR_Y
    surf.fill(WALL_BASE, (0, 0, width, floor))
    for x in range(60, width, 120):
        surf.fill(WALL_ALT, (x, 0, 60, floor))
    surf.fill(WAIN_BASE, (0, 580, width, floor - 580))
    for x in range(0, width, 120):
        surf.fill(WAIN_LINE, (x, 580, 2, floor - 580))
        surf.fill(WAIN_LINE, (x + 120, 580, 2, floor - 580))
    surf.fill(RAIL, (0, 574, width, 6))
    surf.fill(BASEBOARD, (0, floor - 6, width, 6))


def _paint_door(surf, spec):
    if not spec:
        return
    x, y, w, h = spec
    surf.fill((20, 16, 12), (x - 4, y - 4, w + 8, h + 8))
    surf.fill(FRAME, (x, y, w, h))
    surf.fill(BODY, (x + 6, y + 6, w - 12, h - 6))
    surf.fill(BODY_DARK, (x + 16, y + 18, w - 32, h - 42))
    pygame.draw.circle(surf, LIGHT, (x + w - 16, y + h // 2), 5)


def _paint_window(surf, spec):
    if not spec:
        return
    x, y, w, h = spec
    surf.fill(FRAME, (x, y, w, h))
    surf.fill(GLASS, (x + 10, y + 10, w - 20, h - 20))
    pygame.draw.circle(surf, MOON, (x + w - 38, y + 26), 15)
    for sx, sy in ((30, 26), (52, 52), (70, 40), (44, 84), (90, 66)):
        surf.fill(STAR, (x + sx, y + sy, 3, 3))
    surf.fill(FRAME, (x + w // 2 - 2, y + 10, 4, h - 20))
    surf.fill(FRAME, (x + 10, y + h // 2 - 2, w - 20, 4))
    surf.fill(RAIL, (x - 8, y + h, w + 16, 8))


def _paint_picture(surf, rect, kind):
    surf.fill(FRAME, rect)
    inner = rect.inflate(-14, -14)
    if kind == "ship":
        surf.fill((18, 24, 42), inner)
        surf.fill((16, 34, 40), (inner.x, inner.bottom - inner.h // 4, inner.w, inner.h // 4))
        pygame.draw.polygon(surf, (20, 16, 12), [
            (inner.centerx, inner.y + inner.h * 3 // 4),
            (inner.centerx - 14, inner.y + inner.h * 5 // 8),
            (inner.centerx + 14, inner.y + inner.h * 5 // 8),
        ])
        pygame.draw.polygon(surf, (232, 226, 208), [
            (inner.centerx, inner.y + inner.h // 2),
            (inner.centerx + 12, inner.y + inner.h * 5 // 8 - 2),
            (inner.centerx, inner.y + inner.h * 5 // 8 - 2),
        ])
    else:
        surf.fill((52, 46, 60), inner)
        pygame.draw.circle(surf, (198, 180, 160), (inner.centerx, inner.y + inner.h // 3), inner.h // 6)
        pygame.draw.ellipse(surf, (120, 90, 84), (inner.centerx - inner.w // 3, inner.y + inner.h // 2, inner.w * 2 // 3, inner.h // 2))


def _paint_lamp(surf, spec):
    if not spec:
        return
    x, top = spec
    glow = pygame.Surface((90, 70), pygame.SRCALPHA)
    pygame.draw.ellipse(glow, (220, 190, 120, 60), (0, 0, 90, 70))
    surf.blit(glow, (x - 45, top - 62))
    surf.fill(LEG, (x - 2, top + 22, 4, FLOOR_Y - top - 22))
    surf.fill(LEG, (x - 14, FLOOR_Y - 6, 28, 6))
    pygame.draw.polygon(surf, (188, 168, 132), [(x - 24, top), (x + 24, top), (x + 14, top + 40), (x - 14, top + 40)])
    surf.fill(LIGHT, (x - 2, top + 4, 4, 30))


def _paint_rug(surf, spec):
    if not spec:
        return
    x, y, w, h = spec
    surf.fill(RUG_EDGE, (x, y, w, h))
    surf.fill(RUG, (x + 4, y + 4, w - 8, h - 8))
    surf.fill(RUG_EDGE, (x + 10, y + 10, w - 20, h - 20))
    surf.fill(RUG, (x + 14, y + 14, w - 28, h - 28))
    for fx in range(x + 2, x + w - 2, 6):
        surf.fill(LIGHT, (fx, y - 3, 2, 3))
        surf.fill(LIGHT, (fx, y + h, 2, 3))


def _paint_furniture(surf, rect, kind):
    if rect.height > 30:
        _paint_solid_furniture(surf, rect, kind)
    else:
        _paint_open_furniture(surf, rect, kind)


def _paint_solid_furniture(surf, rect, kind):
    # Full-height pieces (height > 30): the hitbox is solid to the floor, so
    # paint the complete piece -- a lighter top face marks the landing surface,
    # then the body and a base plinth. No deck surface covers these (backbone
    # skips blitting one), so everything is drawn here.
    top = rect.top
    left = rect.left
    w = rect.width
    floor = FLOOR_Y

    if kind == "stool":
        surf.fill((146, 116, 80), (left, top, w, 6))
        surf.fill(BODY, (left, top + 6, w, floor - top - 6))
        surf.fill(BODY_DARK, (left, top + 6, w, 2))
        surf.fill(BODY_DARK, (left, top + 6, 3, floor - top - 6))
        surf.fill(BODY_DARK, (left + w - 3, top + 6, 3, floor - top - 6))
        mid = top + (floor - top) // 2
        surf.fill(BODY_DARK, (left + 4, mid, w - 8, 2))
        surf.fill(BODY_DARK, (left - 2, floor - 8, w + 4, 8))
        return

    if kind == "crates":
        surf.fill((146, 116, 80), (left, top, w, 4))
        surf.fill(BODY, (left, top + 4, w, 22))
        surf.fill(BODY_DARK, (left, top + 4, w, 2))
        pygame.draw.line(surf, BODY_DARK, (left + 2, top + 6), (left + w - 2, top + 24), 2)
        pygame.draw.line(surf, BODY_DARK, (left + w - 2, top + 6), (left + 2, top + 24), 2)
        surf.fill(BODY_DARK, (left, top + 26, w, 2))
        surf.fill(BODY, (left, top + 28, w, 22))
        surf.fill(BODY_DARK, (left, top + 28, w, 2))
        pygame.draw.line(surf, BODY_DARK, (left + 2, top + 30), (left + w - 2, top + 48), 2)
        surf.fill(BODY_DARK, (left, top + 50, w, 2))
        surf.fill(BODY, (left, top + 52, w, 12))
        for px in range(left + 4, left + w - 2, 12):
            surf.fill(BODY_DARK, (px, top + 52, 2, 12))
        surf.fill(BODY_DARK, (left, floor - 6, w, 6))
        return

    if kind == "wardrobe":
        surf.fill(BODY_DARK, (left - 2, top, w + 4, 10))
        surf.fill((146, 116, 80), (left, top, w, 2))
        surf.fill(BODY, (left, top + 10, w, floor - top - 16))
        cx = left + w // 2
        surf.fill(BODY_DARK, (cx, top + 12, 2, floor - top - 20))
        for kx in (cx - 16, cx + 14):
            pygame.draw.circle(surf, LIGHT, (kx, top + 22), 3)
        surf.fill(BODY_DARK, (left + w - 10, top + 14, 6, floor - top - 26))
        surf.fill(BODY_DARK, (left - 2, floor - 8, w + 4, 8))
        return

    surf.fill((146, 116, 80), (left, top, w, 8))
    surf.fill(BODY_DARK, (left, top + 8, w, 2))
    body_bottom = floor - 8
    surf.fill(BODY, (left, top + 10, w, body_bottom - top - 10))
    for bx in (left + 8, left + w // 2 - 3, left + w - 11):
        surf.fill((70, 74, 84), (bx, top + 12, 4, body_bottom - top - 14))
    mid = top + 12 + (body_bottom - top - 14) // 2
    pygame.draw.rect(surf, LIGHT, (left + w // 2 - 6, mid - 8, 12, 16))
    pygame.draw.circle(surf, (40, 28, 18), (left + w // 2, mid + 2), 2)
    surf.fill(BODY_DARK, (left, floor - 8, w, 8))


def _paint_open_furniture(surf, rect, kind):
    # Thin slabs (height <= 30): the hitbox is walk-under, so render a body
    # that ends at the standing-head line (654) with legs running to the floor
    # and the space between them open -- the player walks under, not through.
    body_top = rect.bottom
    body_left = rect.left
    body_w = rect.width
    body_h = HEAD_LINE - body_top

    if kind == "loft":
        surf.fill(BODY, (rect.left, body_top, rect.width, 26))
        surf.fill(BODY_DARK, (rect.left, body_top, rect.width, 3))
        surf.fill((62, 45, 30), (rect.left, body_top, rect.width, 2))
        for bx in (rect.left + 8, rect.right - 14):
            pygame.draw.polygon(surf, BODY_DARK, [
                (bx, body_top + 12), (bx + 6, body_top + 12),
                (bx + 10, body_top + 28), (bx - 4, body_top + 28),
            ])
        bx = rect.left + 6
        for color in BOOKS:
            surf.fill(color, (bx, rect.top - 12, 12, 12))
            bx += 14
        return

    surf.fill(BODY, (body_left, body_top, body_w, body_h))
    surf.fill(BODY_DARK, (body_left, body_top, body_w, 2))
    surf.fill(BODY_DARK, (body_left, body_top, 3, body_h))
    surf.fill(BODY_DARK, (body_left + body_w - 3, body_top, 3, body_h))
    surf.fill((62, 45, 30), (body_left, body_top + body_h, body_w, 2))

    leg_w = 12
    surf.fill(LEG, (body_left + 6, HEAD_LINE, leg_w, FLOOR_Y - HEAD_LINE))
    surf.fill(LEG, (body_left + body_w - 6 - leg_w, HEAD_LINE, leg_w, FLOOR_Y - HEAD_LINE))

    if kind == "bed":
        surf.fill(BODY_DARK, (rect.left + 4, rect.top - 26, 34, body_top - rect.top + 26))
        surf.fill(PILLOW, (rect.left + 40, rect.top - 4, 74, 14))
        surf.fill(BLANKET, (rect.left + 118, rect.top - 4, rect.width - 122, 14))
    elif kind == "nightstand":
        for ly in (body_top + body_h // 3, body_top + body_h * 2 // 3):
            surf.fill(BODY_DARK, (body_left + 6, ly, body_w - 12, 2))
            for hx in (body_left + body_w // 2 - 8, body_left + body_w // 2 + 4):
                pygame.draw.circle(surf, LIGHT, (hx, ly + 6), 2)
    elif kind == "desk":
        surf.fill(BODY_DARK, (body_left + 4, body_top + body_h, body_w - 8, 3))
        surf.fill(PLANT_POT, (rect.left + 12, rect.top - 24, 26, 24))
        pygame.draw.circle(surf, PLANT, (rect.left + 25, rect.top - 32), 12)
        pygame.draw.circle(surf, PLANT, (rect.left + 16, rect.top - 38), 9)
        pygame.draw.circle(surf, PLANT, (rect.left + 34, rect.top - 38), 9)
    else:
        surf.fill(BODY_DARK, (body_left + 4, body_top + body_h // 2, body_w - 8, 2))
        pygame.draw.circle(surf, LIGHT, (body_left + body_w // 2, body_top + body_h // 2 + 6), 3)
