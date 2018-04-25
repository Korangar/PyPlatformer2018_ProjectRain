from api.graphics.component import AutoGraphicsComponent, graphics_for
from api.graphics.camera import Camera
from api.graphics.drawing import C_D_GRAY, C_BLACK, gfxdraw, transform, Surface
from api.scene import SceneContent
from api.utilities.tile_grid import Grid, Tile
from api.utilities.vector import *


class TileGridRenderer(SceneContent):
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
        self.bg_prepared: Surface = None
        self.prepare_background()

    def prepare_background(self):
        target_dim = Vector2(*v_mul(self.target.grid_size(), self.target.ppt))
        self.bg_prepared = Surface(target_dim)
        for x, col in enumerate(self.target.tile_grid()):
            for y, pos in enumerate(col):
                rect = (v_mul((x, y), self.target.ppt), (self.target.ppt, self.target.ppt))
                color = pos.tile_info.get("color", C_BLACK)
                Surface.fill(self.bg_prepared, color, rect)
                gfxdraw.rectangle(self.bg_prepared, rect, C_D_GRAY)

    def draw(self, camera: Camera) -> None:
        bg_pos = v_mul(camera.view_origin(), self.target.ppt)
        bg_dim = v_mul(camera.projection.dimension, self.target.ppt/camera.projection.pixels_per_tile)
        if camera.projection.pixels_per_tile != self.target.ppt:
            bg_view = self.bg_prepared.subsurface((bg_pos, bg_dim))
            transform.scale(bg_view, camera.render_target.get_size(), camera.render_target)
        else:
            camera.render_target.blit(self.bg_prepared, (0, 0), (bg_pos, bg_dim))
