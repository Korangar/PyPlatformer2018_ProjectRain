import pygame as _pygame
from typing import *

_pygame.init()
_pygame.display.init()


class PyGameDisplay:
    def __init__(self, resolution: Tuple[int, int]=(0, 0), depth: int=0, full_screen: bool=True):
        flags = 0
        if full_screen:
            from pygame import FULLSCREEN
            flags += FULLSCREEN
        self.canvas: _pygame.Surface = _pygame.display.set_mode(resolution, flags, depth)
        self.resolution: Tuple[int, int] = self.canvas.get_size()
        self.flip: Callable[[], None] = _pygame.display.flip
