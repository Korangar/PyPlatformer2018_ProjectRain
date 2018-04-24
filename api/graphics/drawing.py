import pygame.freetype as freetype
import pygame.gfxdraw as gfxdraw
import pygame.image as image
import pygame.transform as transform
from pygame import Surface

import typing

freetype.init()


RGB = typing.Tuple[int, int, int]
RGBA = typing.Tuple[int, int, int, int]

C_WHITE = (255, 255, 255)
C_L_GRAY = (155, 155, 155)
C_D_GRAY = (100, 100, 100)
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_GREEN = (0, 255, 0)
C_BLUE = (0, 0, 255)
C_YELLOW = (255, 255, 0)
C_SOMETHING = (0, 255, 255)


def f_default(size: float, bold=0, italic=0, constructor=None) -> freetype.Font:
    return freetype.SysFont(freetype.get_default_font(), size, bold, italic, constructor)
