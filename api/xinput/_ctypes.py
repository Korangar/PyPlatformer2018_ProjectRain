# XINPUT WRAPPER FOR PYTHON

import ctypes
from enum import Enum


# Import the input driver
try:
    _xinput = ctypes.windll.xinput9_1_0
except ImportError:
    raise ImportError("Could not load the Xinput.dll")


# Declare constants
# C types
U_BYTE = 255
U_SHORT = 65535
C_SHORT = 32767

# MS error codes
ERROR_NOT_CONNECTED = 1167


# Labels
class AnalogInputs(Enum):
    trigger_l = "trigger_l"
    trigger_r = "trigger_r"
    analog_l = "analog_l"
    analog_r = "analog_r"


# Button masks
class ButtonFlags(Enum):
    d_pad_u = 0x0001
    d_pad_d = 0x0002
    d_pad_l = 0x0004
    d_pad_r = 0x0008
    button_str = 0x0010
    button_bck = 0x0020
    stick_l = 0x0040
    stick_r = 0x0080
    shoulder_l = 0x0100
    shoulder_r = 0x0200
    button_a = 0x1000
    button_b = 0x2000
    button_x = 0x4000
    button_y = 0x8000


# XInput structures
class XINPUTGAMEPAD(ctypes.Structure):
    _fields_ = [("wButtons", ctypes.c_ushort),
                ("bLeftTrigger", ctypes.c_ubyte),
                ("bRightTrigger", ctypes.c_ubyte),
                ("sThumbLX", ctypes.c_short),
                ("sThumbLY", ctypes.c_short),
                ("sThumbRX", ctypes.c_short),
                ("sThumbRY", ctypes.c_short)]


class XINPUTSTATE(ctypes.Structure):
    _fields_ = [("dwPacketNumber", ctypes.c_uint32),
                ("Gamepad", XINPUTGAMEPAD)]


class XINPUTVIBRATION(ctypes.Structure):
    _fields_ = [("wLeftMotorSpeed", ctypes.c_ushort),
                ("wRightMotorSpeed", ctypes.c_ushort)]


# XInput functions
# getState
XInputGetState = _xinput.XInputGetState
XInputGetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUTSTATE)]
XInputGetState.resttype = ctypes.c_uint
# setState
XInputSetState = _xinput.XInputSetState
XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUTVIBRATION)]
XInputSetState.restype = ctypes.c_uint
