from api.graphics import Camera, AutoGraphicsComponent
from api.graphics import C_D_GRAY, C_BLACK
from api.graphics import Surface, gfxdraw, transform
from api.graphics.projection import *
from api.scene import SceneContent
from api.utilities.tile_grid import Grid, Tile
from api.utilities.vector import *


class TileGridRenderer(SceneContent):
    def __init__(self, tile_grid: Grid[Tile], pixels: int) -> None:
        super().__init__(Point(0, 0))
        self.tile_grid = tile_grid
        self.size = Vector2(len(self.tile_grid), len(self.tile_grid[0]))
        self.ppt = pixels


@graphics_instruction(TileGridRenderer)
class TileGridGraphics(AutoGraphicsComponent[TileGridRenderer]):
    def __init__(self, target: TileGridRenderer):
        super().__init__(target)
        self.target: TileGridRenderer
        self.bg_prepared: Surface = None
        self.bg_projection: Projection = None
        self.prepare_background()

    def prepare_background(self):
        target_dim = Vector2(*v_mul(self.target.size, self.target.ppt))
        self.bg_prepared = Surface(target_dim)
        self.bg_projection = Projection(source_off=Vector2(0, 0),
                                        source_dim=self.target.size,
                                        target_off=Vector2(0, 0),
                                        target_dim=Vector2(*target_dim),
                                        inverse_v=True,
                                        inverse_h=False)
        for x, col in enumerate(self.target.tile_grid):
            for y, pos in enumerate(col):
                rect = (v_mul((x, y), self.target.ppt), (self.target.ppt, self.target.ppt))
                color = pos.tile_info.get("color", C_BLACK)
                Surface.fill(self.bg_prepared, color, rect)
                gfxdraw.rectangle(self.bg_prepared, rect, C_D_GRAY)

    def draw(self, camera: Camera) -> None:
        bg_off = v_mul(camera.get_view_origin(), self.target.ppt)
        bg_dim = v_mul(camera.view.source_dim, self.target.ppt)
        if camera.ppt != self.target.ppt:
            bg_view = self.bg_prepared.subsurface((bg_off, bg_dim))
            transform.scale(bg_view, camera.target.get_size(), camera.target)
        else:
            camera.target.blit(self.bg_prepared, (0, 0), (bg_off, bg_dim))
