import ctypes

KEY_ID_TO_SCANCODE = {8: 14, 9: 15, 13: 28, 19: 69, 20: 58, 27: 1, 32: 57, 33: 73, 34: 81, 35: 79, 36: 71, 37: 75,
                      38: 72, 39: 77, 40: 80, 44: 55, 45: 82, 46: 83, 48: 11, 49: 2, 50: 3, 51: 4, 52: 5, 53: 6, 54: 7,
                      55: 8, 56: 9, 57: 10, 65: 30, 66: 48, 67: 46, 68: 32, 69: 18, 70: 33, 71: 34, 72: 35, 73: 23,
                      74: 36, 75: 37, 76: 38, 77: 50, 78: 49, 79: 24, 80: 25, 81: 16, 82: 19, 83: 31, 84: 20, 85: 22,
                      86: 47, 87: 17, 88: 45, 89: 44, 90: 21, 91: 91, 92: 92, 93: 93, 96: 82, 97: 79, 98: 80, 99: 81,
                      100: 75, 101: 76, 102: 77, 103: 71, 104: 72, 105: 73, 106: 55, 107: 78, 109: 74, 110: 83, 111: 53,
                      112: 59, 113: 60, 114: 61, 115: 62, 116: 63, 117: 64, 118: 65, 119: 66, 120: 67, 121: 68, 122: 87,
                      123: 88, 144: 69, 145: 70, 160: 42, 161: 54, 162: 29, 163: 29, 164: 56, 165: 56, 186: 26, 187: 27,
                      188: 51, 189: 53, 190: 52, 191: 43, 192: 39, 219: 12, 220: 41, 221: 13, 222: 40, 226: 86}

EXTENDED_KEY_IDS = [173, 144, 46, 33, 34, 35, 36, 165, 166, 167, 40, 44, 45, 174, 175, 176, 177, 178, 179, 161, 163, 91,
                    92, 93, 37, 38, 39, 111]

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]


class InputI(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", InputI)]


def press_key(vkey_code, extended_flag=None):
    if extended_flag is None:
        extended_flag = int(vkey_code in EXTENDED_KEY_IDS)

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(vkey_code, KEY_ID_TO_SCANCODE.get(vkey_code, 0), extended_flag, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(vkey_code, extended_flag=None):
    if extended_flag is None:
        extended_flag = int(vkey_code in EXTENDED_KEY_IDS)

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(vkey_code, KEY_ID_TO_SCANCODE.get(vkey_code, 0), 0x0002 + extended_flag, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def press_mouse_key(vkey_code):
    # down
    # left: 0x2
    # right: 0x8
    # middle: 0x20
    # x button: 0x80
    data = 0x0
    flags = 0x0
    if vkey_code == 0x1:
        flags = 0x2
    elif vkey_code == 0x2:
        flags = 0x8
    elif vkey_code == 0x4:
        flags = 0x20
    elif vkey_code == 0x5:
        data = 0x1
        flags = 0x80
    elif vkey_code == 0x6:
        data = 0x2
        flags = 0x80

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.mi = MouseInput(0, 0, data, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_mouse_key(vkey_code):
    # up
    # left: 0x4
    # right: 0x10
    # middle: 0x40
    # x button: 0x100
    data = 0x0
    flags = 0x0
    if vkey_code == 0x1:
        flags = 0x4
    elif vkey_code == 0x2:
        flags = 0x10
    elif vkey_code == 0x4:
        flags = 0x40
    elif vkey_code == 0x5:
        data = 0x1
        flags = 0x100
    elif vkey_code == 0x6:
        data = 0x2
        flags = 0x100

    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.mi = MouseInput(0, 0, data, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def press_key_u(vkey_code):
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(0, vkey_code, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key_u(vkey_code):
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(0, vkey_code, 0x0006, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
