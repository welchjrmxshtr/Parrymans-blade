import pygame

HUD_COLOR = (210, 210, 225)
HUD_MARGIN = 8


def draw_hud(screen, font, level):
    label = f"{level.WORLD_INDEX + 1}-{level.LEVEL_INDEX + 1}  {level.WORLD['name']} — {level.LEVEL['name']}"
    text = font.render(label, HUD_COLOR)
    screen.blit(text, (HUD_MARGIN, HUD_MARGIN))
