from api.sax_engine.tile_grid import Tile
from api.sax_engine.core.systems.graphics.drawing import C_L_GRAY

t_wall = Tile("Wall", {"color": C_L_GRAY})
t_air = Tile("Air", {})
tile_map = [[t_wall] * 150] + \
           [[t_wall] + [t_air] * 148 + [t_wall]] * 48 + \
           [[t_wall] + [t_wall] * 148 + [t_wall]] + \
           [[t_wall] + [t_air] * 148 + [t_wall]] * 50 + \
           [[t_wall] * 150]

tile_map = list(zip(*tile_map))
