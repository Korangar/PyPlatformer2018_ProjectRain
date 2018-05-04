# Enumeration Based Microsoft XInput - Gamepad API

from ._ctypes import *

from typing import *
from enum import Enum
from time import time as time_now

__all__ = ['XInputGamepad', 'GamePadState', 'AnalogStick', 'ButtonFlags', 'AnalogInputs']

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


# Singleton-like gamepad class
# Enumeration approach to the Singleton Pattern
def update_gamepads():
    for g in XInputGamepad:
        if g.disabled:
            pass
        elif g.connected() or time_now() - g.last_update > 5:
            # update connected devices or try to reconnect after 5 secs
            g.fetch_input()


# Updates all xinput devices and checks connections
def create_neutral_state(dz) -> GamePadState:
    neutral_as = create_analog_stick(0, 0, dz)
    return GamePadState(analog_l=neutral_as, analog_r=neutral_as,
                        trigger_l=.0, trigger_r=.0, events={},
                        buttons={b: False for b in ButtonFlags})


# Instantiation helper for a neutral gamepad state
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


# Instantiation helper for analog sticks
class XInputGamepad(Enum):
    pad_0 = 0
    pad_1 = 1
    pad_2 = 2
    pad_3 = 3

    def __init__(self, value):
        # hardware info
        self._raw_id = value
        self._raw_state = XINPUTSTATE()

        # status
        self.enabled = True
        self._connected = False
        self.last_update = time_now()

        # settings
        self.dz = 0.3

        # state
        self.input_state = create_neutral_state(self.dz)
        self.rumble_l = 0
        self.rumble_r = 0

    def connected(self) -> bool:
        return self._connected

    def __repr__(self) -> str:
        return "XGamePad: {}".format(self._raw_id)

    def __str__(self) -> str:
        tmp = "connected" if self._connected else "not connected"
        return "XGamePad:{} ({})".format(self._raw_id, tmp)

    def set_rumble(self, rumble_l: float, rumble_r: float) -> None:
        self.rumble_l = rumble_l
        self.rumble_r = rumble_r
        vibration = XINPUTVIBRATION(int(rumble_l * U_SHORT), int(rumble_r * U_SHORT))
        XInputSetState(self._raw_id, ctypes.byref(vibration))

    def fetch_input(self) -> None:
        self.last_update = time_now()
        success = self._try_fetch_raw()
        if success:
            # analog input
            events = dict()
            game_pad = self._raw_state.Gamepad
            # analog_l
            analog_l = self._read_analog(self.input_state.analog_l,
                                         game_pad.sThumbLX,
                                         game_pad.sThumbLY,
                                         events)
            # analog_r
            analog_r = self._read_analog(self.input_state.analog_r,
                                         game_pad.sThumbRX,
                                         game_pad.sThumbRY,
                                         events)
            # trigger_l
            trigger_l = self._read_trigger(self.input_state.trigger_l,
                                           game_pad.bLeftTrigger,
                                           events)
            # trigger_r
            trigger_r = self._read_trigger(self.input_state.trigger_r,
                                           game_pad.bRightTrigger,
                                           events)
            # digital input
            buttons = dict()
            for btn_code in ButtonFlags:
                self._read_button(btn_code, events, buttons)

            # create new official state
            self.input_state = GamePadState(analog_l=analog_l,
                                            analog_r=analog_r,
                                            trigger_l=trigger_l,
                                            trigger_r=trigger_r,
                                            buttons=buttons,
                                            events=events)

    def _try_fetch_raw(self) -> bool:
        error_code = XInputGetState(self._raw_id, self._raw_state)
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

    def _read_analog(self, old_value, raw_x, raw_y, events):
        new_value = create_analog_stick(raw_x, raw_y, self.dz)
        dx = new_value.x - old_value.x
        dy = new_value.y - old_value.y
        if abs(dx) > 0 or abs(dy) > 0:
            events[AnalogInputs.analog_l] = (dx, dy)
        return new_value

    # noinspection PyMethodMayBeStatic
    def _read_trigger(self, old_value, raw_value, events):
        new_value = raw_value / U_BYTE
        delta = new_value - old_value
        if abs(delta) > 0:
            events[AnalogInputs.trigger_r] = delta
        return new_value

    def _read_button(self, btn_code, events, buttons):
        new_value = (self._raw_state.Gamepad.wButtons & btn_code.value) is not 0
        old_value = self.input_state.buttons[btn_code]
        if not (new_value == old_value):
            events[btn_code] = new_value
        buttons[btn_code] = new_value
        return new_value
