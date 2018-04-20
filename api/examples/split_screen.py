from api.utilities.vector import *
from api.graphics import get_display
from api.scene import SceneContent
from typing import *


def split_screen(*anchors: SceneContent, ppt: int=32) -> Iterator:
    dim = get_display().resolution
    if len(anchors) > 2:
        dim = Vector2(*v_mul(dim, Vector2(0.5, 0.5)))
    elif len(anchors) > 1:
        dim = Vector2(*v_mul(dim, Vector2(0.5, 1)))
    offsets = (Vector2(0, 0),
               Vector2(1, 0),
               Vector2(0, 1),
               Vector2(1, 1))
    return ({'anchor': anchor,
             'target_dim': dim,
             'pixels_per_tile': ppt,
             'source_rel_off': Vector2(-.5, -.5),
             'target_rel_off': offsets[i]} for i, anchor in enumerate(anchors))
