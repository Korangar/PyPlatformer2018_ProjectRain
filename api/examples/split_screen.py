from api.utilities.vector import *
from api.graphics import get_display
from api.scene import SceneContent
from typing import *


def split_screen(anchors: int=1, ppt: int=32) -> Iterator:
    assert 1 <= anchors <= 4
    dim = get_display().resolution
    if len(anchors) > 2:
        dim = Vector2(*v_mul(dim, Vector2(0.5, 0.5)))
    elif len(anchors) > 1:
        dim = Vector2(*v_mul(dim, Vector2(0.5, 1)))
    offsets = (Vector2(0, 0),
               Vector2(1, 0),
               Vector2(0, 1),
               Vector2(1, 1))
    return ({'anchor': Vector2(-.5, -.5),
             'dimension': dim,
             'pixels_per_tile': ppt,
             'screen_position': offsets[i]} for i, anchor in enumerate(anchors))
