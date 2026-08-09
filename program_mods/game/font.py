import pygame


def make_font(size):
    try:
        from pygame.font import Font
        return _PygameFont(Font(None, size))
    except ImportError:
        from pygame import _freetype as ft
        ft.init()
        return _FreetypeFont(ft.Font(None, size))


class _PygameFont:
    def __init__(self, font):
        self._font = font

    def render(self, text, color):
        return self._font.render(text, True, color)


class _FreetypeFont:
    def __init__(self, font):
        self._font = font

    def render(self, text, color):
        surf, rect = self._font.render(text, fgcolor=color)
        return surf
