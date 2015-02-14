import ctypes

import Constants


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


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]


def press_key(vkey_code, extended_flag=None):
    #print('press {}'.format(Constants.id_to_vkey(vkey_code)))
    if extended_flag is None:
        extended_flag = int(vkey_code in Constants.vExtendedKeys)

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vkey_code, get_scan_code(vkey_code), extended_flag, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def scroll(x):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, x, 0x0800, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(vkey_code, extended_flag=None):
    #print('release {}'.format(Constants.id_to_vkey(vkey_code)))
    if extended_flag is None:
        extended_flag = int(vkey_code in Constants.vExtendedKeys)

    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vkey_code, get_scan_code(vkey_code), 0x0002+extended_flag, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_mouse_key(vkey_code):
    # down
    # left: 0x2
    # right: 0x8
    # middle: 0x20
    # x button: 0x80
    data = 0x0
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
    ii_ = Input_I()
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
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, data, flags, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_key_u(vkey_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, vkey_code, 0x0004, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key_u(vkey_code):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, vkey_code, 0x0006, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def get_scan_code(vkey_code):
    if vkey_code in Constants.vKeyToScanCode:
        return Constants.vKeyToScanCode[vkey_code]
    else:
        return 0

if __name__ == '__main__':

    press_key_u(0x20AC)
    release_key_u(0x20AC)
