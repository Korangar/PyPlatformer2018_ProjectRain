# Enumeration Based Microsoft XInput - Gamepad API

from .xinput_wrapper import *
from .xinput_wrapper import _XInputGetState, _XInputSetState

from typing import *
from enum import Enum
from time import time as time_now


EventKeys = Union[AnalogInputs, ButtonFlags]


# Immutable data classes
# State of an analog stick
class AnalogStick(NamedTuple):
    x: float
    y: float
    raw_x: int
    raw_y: int
    dead_zone: float
    magnitude: float


# Input state of XGamePad
class GamePadState(NamedTuple):
    analog_l: AnalogStick
    analog_r: AnalogStick
    trigger_l: float
    trigger_r: float
    buttons: Dict[ButtonFlags, bool]
    events: Dict[EventKeys, Any]


# Instantiation helper for analog sticks
def create_analog_stick(raw_x: int, raw_y: int, dead_zone: float) -> AnalogStick:
    axis_x = raw_x / C_SHORT
    axis_y = raw_y / C_SHORT
    magnitude = (axis_x ** 2 + axis_y ** 2) ** 0.5
    if magnitude > dead_zone:
        dz_factor = (magnitude - dead_zone) / (1 - dead_zone)
        return AnalogStick(x=axis_x / magnitude * dz_factor,
                           y=axis_y / magnitude * dz_factor,
                           raw_x=raw_x,
                           raw_y=raw_y,
                           dead_zone=dead_zone,
                           magnitude=magnitude)
    else:
        return AnalogStick(x=.0,
                           y=.0,
                           raw_x=raw_x,
                           raw_y=raw_y,
                           dead_zone=dead_zone,
                           magnitude=.0)


# Singleton-like gamepad class
# Enumeration approach to the Singleton Pattern
class XInputGamePad(Enum):
    pad_0 = 0
    pad_1 = 1
    pad_2 = 2
    pad_3 = 3

    @staticmethod
    def update_all():
        for g in XInputGamePad:
            if g.disabled:
                pass
            elif g.connected() or time_now() - g.last_update > 5:
                # update connected devices or try to reconnect after 5 secs
                g.fetch_input()

    def __init__(self, value):
        # hardware info
        self._raw_id = value
        self._raw_state = XINPUTSTATE()

        # status
        self.enabled = True
        self._connected = False
        self.last_update = time_now()

        # state
        self.input_state = self.get_neutral_state()
        self.rumble_l = 0
        self.rumble_r = 0

        # settings
        self.default_dz = 0.2

    def connected(self) -> bool:
        return self._connected

    def __repr__(self) -> str:
        return "XGamePad: {}".format(self._raw_id)

    def __str__(self) -> str:
        tmp = "connected" if self._connected else "not connected"
        return "XGamePad:{} ({})".format(self._raw_id, tmp)

    def get_neutral_state(self) -> GamePadState:
        neutral_as = create_analog_stick(0, 0, self.default_dz)
        return GamePadState(analog_l=neutral_as, analog_r=neutral_as,
                            trigger_l=.0, trigger_r=.0, events={},
                            buttons={b: False for b in ButtonFlags})

    def set_rumble(self, rumble_l: float, rumble_r: float) -> None:
        self.rumble_l = rumble_l
        self.rumble_r = rumble_r
        vibration = XINPUTVIBRATION(int(rumble_l * U_SHORT), int(rumble_r * U_SHORT))
        _XInputSetState(self._raw_id, ctypes.byref(vibration))

    def fetch_input(self) -> None:
        self.last_update = time_now()
        success = self._try_fetch_raw()
        if success:
            events = dict()
            buttons = dict()
            game_pad = self._raw_state.Gamepad
            # analog_l
            analog_l = create_analog_stick(game_pad.sThumbLX, game_pad.sThumbLY, self.default_dz)
            old_value = self.input_state.analog_l
            dx = analog_l.x - old_value.x
            dy = analog_l.y - old_value.y
            if abs(dx) > 0 or abs(dy) > 0:
                events[EventKeys.analog_l] = (dx, dy)
            # analog_r
            analog_r = create_analog_stick(game_pad.sThumbRX, game_pad.sThumbRY, self.default_dz)
            old_value = self.input_state.analog_r
            dx = analog_r.x - old_value.x
            dy = analog_r.y - old_value.y
            if abs(dx) > 0 or abs(dy) > 0:
                events[EventKeys.analog_r] = (dx, dy)
            # trigger_l
            trigger_l = game_pad.bLeftTrigger / U_BYTE
            old_value = self.input_state.trigger_l
            delta = trigger_l - old_value
            if abs(delta) > 0:
                events[EventKeys.trigger_l] = delta
            # trigger_r
            trigger_r = game_pad.bRightTrigger / U_BYTE
            old_value = self.input_state.trigger_r
            delta = trigger_r - old_value
            if abs(delta) > 0:
                events[EventKeys.trigger_r] = delta
            # buttons
            for btn_code in ButtonFlags:
                new_value = (game_pad.wButtons & btn_code.value) is not 0
                old_value = self.input_state.buttons[btn_code]
                if not (new_value == old_value):
                    events[btn_code] = new_value
                buttons[btn_code] = new_value
            # apply changes
            self.input_state = GamePadState(analog_l=analog_l,
                                            analog_r=analog_r,
                                            trigger_l=trigger_l,
                                            trigger_r=trigger_r,
                                            buttons=buttons,
                                            events=events)

    def _try_fetch_raw(self) -> bool:
        error_code = _XInputGetState(self._raw_id, self._raw_state)
        if error_code == ERROR_NOT_CONNECTED:
            if self._connected:
                # connection lost
                # update connection status
                self._connected = False
                # reset input fields
                self.input_state = self._neutral_state()
                # disconnected!
                print(self)
            return False
        else:
            if not self._connected:
                # connection established
                # update connection status
                self._connected = True
                # deactivate vibration
                self.set_rumble(rumble_l=.0, rumble_r=.0)
                # reconnected!
                print(self)
            return True
