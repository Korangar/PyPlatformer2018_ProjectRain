from api.sax_engine.core.systems.input.component import AutoInputComponent, input_for
from api.xinput import *
from ..player import Player
from ..event_id import PlayerEventId

jump = ButtonFlags.button_a
shoot = ButtonFlags.button_x
aiming = AnalogInputs.trigger_r
trigger_threshold = 0.5


@input_for(Player)
class PlayerInput(AutoInputComponent[Player]):
    def __init__(self, target: Player):
        super().__init__(target)
        self.target.input_data.gamepad = tuple(XInputGamepad)[self.target.number]

    def update(self) -> None:
        data = self.target.input_data

        old_state = data.gamepad.input_state
        data.gamepad.fetch_input()
        new_state = data.gamepad.input_state

        # get movement
        data.player_directional = new_state.analog_l

        # get jump
        if jump in new_state.events:
            msg = (PlayerEventId.press_jump
                   if new_state.events[jump] else
                   PlayerEventId.release_jump)
            self.target.push_event(msg)

        # get shoot
        if shoot in new_state.events:
            msg = (PlayerEventId.press_shoot
                   if new_state.events[shoot] else
                   PlayerEventId.release_shoot)
            self.target.push_event(msg)

        # get aiming
        now, before = tuple(s > trigger_threshold for s in (new_state.trigger_r, old_state.trigger_r))

        if now and not before:
            self.target.push_event(PlayerEventId.press_take_aim)
        elif before and not now:
            self.target.push_event(PlayerEventId.release_take_aim)


