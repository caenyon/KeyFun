import ctypes

# mapping from virtual key ids to scancodes. this list was created with an activated german keyboard layout and may be
# incomplete.
KEY_ID_TO_SCANCODE = {8: 14, 9: 15, 13: 28, 19: 69, 20: 58, 27: 1, 32: 57, 33: 73, 34: 81, 35: 79, 36: 71, 37: 75,
                      38: 72, 39: 77, 40: 80, 44: 55, 45: 82, 46: 83, 48: 11, 49: 2, 50: 3, 51: 4, 52: 5, 53: 6, 54: 7,
                      55: 8, 56: 9, 57: 10, 65: 30, 66: 48, 67: 46, 68: 32, 69: 18, 70: 33, 71: 34, 72: 35, 73: 23,
                      74: 36, 75: 37, 76: 38, 77: 50, 78: 49, 79: 24, 80: 25, 81: 16, 82: 19, 83: 31, 84: 20, 85: 22,
                      86: 47, 87: 17, 88: 45, 89: 44, 90: 21, 91: 91, 92: 92, 93: 93, 96: 82, 97: 79, 98: 80, 99: 81,
                      100: 75, 101: 76, 102: 77, 103: 71, 104: 72, 105: 73, 106: 55, 107: 78, 109: 74, 110: 83, 111: 53,
                      112: 59, 113: 60, 114: 61, 115: 62, 116: 63, 117: 64, 118: 65, 119: 66, 120: 67, 121: 68, 122: 87,
                      123: 88, 144: 69, 145: 70, 160: 42, 161: 54, 162: 29, 163: 29, 164: 56, 165: 56, 186: 26, 187: 27,
                      188: 51, 189: 53, 190: 52, 191: 43, 192: 39, 219: 12, 220: 41, 221: 13, 222: 40, 226: 86}

# this list contains the virtual key ids which should be sent with the extended bit set.
EXTENDED_KEY_IDS = [173, 144, 46, 33, 34, 35, 36, 165, 166, 167, 40, 44, 45, 174, 175, 176, 177, 178, 179, 161, 163, 91,
                    92, 93, 37, 38, 39, 111]

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004

MOUSE_KEY_ID_TO_SENDKEYS_FLAG = {0x1: 0x0002, 0x2: 0x0008, 0x4: 0x0020, 0x5: 0x0080, 0x6: 0x0080}

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


def send_keyboard_input(key_id, down, unicode_key=False, extended_flag=None):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646271(v=vs.85).aspx

    flags = 0
    if not down:
        flags += KEYEVENTF_KEYUP

    if unicode_key:
        # For a unicode key, key_id must be 0 and scancode must contain the unicode key id.
        scancode = key_id
        key_id = 0
        flags += KEYEVENTF_UNICODE
    else:
        scancode = KEY_ID_TO_SCANCODE.get(key_id, 0)  # If key_id is not in list, take 0 as default.
        if (extended_flag is not None and extended_flag) or (extended_flag is None and key_id in EXTENDED_KEY_IDS):
            flags += KEYEVENTF_EXTENDEDKEY

    # Create structs and send input
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.ki = KeyBdInput(key_id, scancode, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def send_mouse_input(key_id, down):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/ms646273(v=vs.85).aspx

    flags = MOUSE_KEY_ID_TO_SENDKEYS_FLAG[key_id]
    if not down:
        flags *= 2
    data = key_id - 0x4 if key_id > 0x4 else 0

    # Create structs and send input
    extra = ctypes.c_ulong(0)
    ii_ = InputI()
    ii_.mi = MouseInput(0, 0, data, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
