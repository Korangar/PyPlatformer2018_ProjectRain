from api.sax_engine.core.systems.graphics.component import AutoGraphicsComponent, graphics_for
from api.sax_engine.core.systems.graphics.projection import Projection
from api.sax_engine.core.systems.graphics.camera import Camera
from api.sax_engine.core.systems.graphics.drawing import C_D_GRAY, C_BLACK, draw, transform, Surface
from api.sax_engine.core import ContentEntity
from api.sax_engine.vector import *

__all__ = ['TileGridRenderer']
C_D_GRAY = v_mul(C_D_GRAY, 0.2)


class TileGridRenderer(ContentEntity):
    def __init__(self, default_resolution: int=32) -> None:
        super().__init__()
        self.ppt = default_resolution

    def tile_grid(self):
        return self.scene.tile_grid

    def grid_size(self):
        tg = self.tile_grid()
        return Vector2(len(tg), len(tg[0]))


@graphics_for(TileGridRenderer)
class TileGridGraphics(AutoGraphicsComponent[TileGridRenderer]):
    def __init__(self, target: TileGridRenderer):
        super().__init__(target)
        self.sorting = -math.inf
        grid_size = self.target.grid_size()
        target_dim = Vector2(*v_mul(grid_size, self.target.ppt))
        self.bg_prepared = Surface(target_dim)
        self.projection = Projection(
            anchor=Vector2(0, 0),
            dimension=self.bg_prepared.get_size(),
            inverse_v=True
        )
        for x, col in enumerate(self.target.tile_grid()):
            for y, pos in enumerate(col):
                rect = (v_mul((x, grid_size[1]-(y + 1)), self.target.ppt), (self.target.ppt, self.target.ppt))
                color = pos.tile_info.get("color", C_BLACK)
                Surface.fill(self.bg_prepared, color, rect)
                draw.rectangle(self.bg_prepared, rect, C_D_GRAY)

    def draw(self, camera: Camera) -> None:
        bg_dim = v_mul(camera.projection.dimension, self.target.ppt / camera.projection.pixels_per_tile)
        bg_pos = v_sub(self.projection.project(camera.view_origin()), (0, bg_dim[1]))
        if camera.projection.pixels_per_tile != self.target.ppt:
            bg_view = self.bg_prepared.subsurface((bg_pos, bg_dim))
            transform.scale(bg_view, camera.render_target.get_size(), camera.render_target)
        else:
            camera.render_target.blit(self.bg_prepared, (0, 0), (bg_pos, bg_dim))
