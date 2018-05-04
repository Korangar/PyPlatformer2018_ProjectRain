import pygame.gfxdraw as draw
from pygame import image
from pygame import transform
from pygame import freetype
from pygame import Surface

__all__ = ['draw', 'image', 'transform', 'freetype', 'Surface', 'f_default']
freetype.init()


def f_default(size: float, bold=0, italic=0, constructor=None) -> freetype.Font:
    return freetype.SysFont(freetype.get_default_font(), size, bold, italic, constructor)


