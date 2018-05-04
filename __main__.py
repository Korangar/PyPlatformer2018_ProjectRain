import api.sax_engine.core as core
from api.sax_engine.core import input
from api.sax_engine.core import physics
from api.sax_engine.core import graphics
from api.sax_engine.events import yield_api_events
from api.sax_engine.timing.time import time_ms

updates_per_sec = 60
update_delay = 1000/updates_per_sec
delta_time = update_delay/1000
avg_redraw_rate = 0.0
avg_update_delay = 0.0


if __name__ == "__main__":
    # init
    graphics.init_display(full_screen=True)

    from start_scene import initialize
    initialize()

    # game loop
    last_update = time_ms()
    update_loops_max = 5
    update_loops = 0
    while True:
        # update timing parameters
        time_since_update = time_ms() - last_update

        # event pump for pygame
        yield_api_events()

        if time_since_update > update_delay and update_loops < update_loops_max:
            # timing
            last_update += update_delay
            update_loops += 1

            # set current time step
            core.set_delta_time(delta_time)

            # update input
            input.update()
            # update physics
            physics.update()
            # update core
            core.update()
        else:
            # timing
            update_loops = 0

            # update graphics
            graphics.update()
