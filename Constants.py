# -*- coding: utf-8 -*-
"""
Constants contains several functions and constants useful in other modules.
"""
__author__ = 'Felix'
import re

import pyHook


vKeyToScanCode = {8: 14, 9: 15, 13: 28, 19: 69, 20: 58, 27: 1, 32: 57, 33: 73, 34: 81, 35: 79, 36: 71, 37: 75, 38: 72,
                  39: 77, 40: 80, 44: 55, 45: 82, 46: 83, 48: 11, 49: 2, 50: 3, 51: 4, 52: 5, 53: 6, 54: 7, 55: 8,
                  56: 9, 57: 10, 65: 30, 66: 48, 67: 46, 68: 32, 69: 18, 70: 33, 71: 34, 72: 35, 73: 23, 74: 36, 75: 37,
                  76: 38, 77: 50, 78: 49, 79: 24, 80: 25, 81: 16, 82: 19, 83: 31, 84: 20, 85: 22, 86: 47, 87: 17,
                  88: 45, 89: 44, 90: 21, 91: 91, 92: 92, 93: 93, 96: 82, 97: 79, 98: 80, 99: 81, 100: 75, 101: 76,
                  102: 77, 103: 71, 104: 72, 105: 73, 106: 55, 107: 78, 109: 74, 110: 83, 111: 53, 112: 59, 113: 60,
                  114: 61, 115: 62, 116: 63, 117: 64, 118: 65, 119: 66, 120: 67, 121: 68, 122: 87, 123: 88, 144: 69,
                  145: 70, 160: 42, 161: 54, 162: 29, 163: 29, 164: 56, 165: 56, 173: 0, 176: 0, 177: 0, 178: 0, 179: 0,
                  186: 26, 187: 27, 188: 51, 189: 53, 190: 52, 191: 43, 192: 39, 219: 12, 220: 41, 221: 13, 222: 40,
                  226: 86}

vExtendedKeys = [173, 144, 46, 33, 34, 35, 36, 165, 166, 167, 40, 44, 45, 174, 175, 176, 177, 178, 179, 161, 163, 91,
                 92, 93, 37, 38, 39, 111]

mouse_codes = {0x0200: "WM_MOUSEMOVE", 0x0201: "WM_LBUTTONDOWN", 0x0202: "WM_LBUTTONUP", 0x0204: "WM_RBUTTONDOWN",
               0x0205: "WM_RBUTTONUP", 0x0207: "WM_MBUTTONDOWN", 0x0208: "WM_MBUTTONUP", 0x020A: "WM_MOUSEWHEEL",
               0x020B: "WM_XBUTTONDOWN", 0x020C: "WM_XBUTTONUP", 0x020E: "WM_MOUSEHWHEEL", }

vk_to_id = {}
for key in pyHook.HookConstants.vk_to_id:
    vk_to_id[key] = pyHook.HookConstants.vk_to_id[key]
for i in range(0x41, 0x5A + 1) + range(0x30, 0x39 + 1):
    vk_to_id['VK_' + chr(i)] = i
vk_to_id['VK_XBUTTON1'] = 0x05
vk_to_id['VK_XBUTTON2'] = 0x06
vk_to_id['VK_NRETURN'] = 0x88

id_to_vk = dict([(v, k) for k, v in vk_to_id.items()])

simpleModRaw = [('Q', 'NEXT'), ('W', 'BACK'), ('E', 'UP'), ('R', 'DELETE'), ('T', 'PRIOR'), ('A', 'HOME'),
                ('S', 'LEFT'), ('D', 'DOWN'), ('F', 'RIGHT'), ('G', 'END')]
simpleMod = {}
for i, j in simpleModRaw:
    simpleMod[vk_to_id['VK_' + i]] = vk_to_id['VK_' + j]


def id_to_vkey(code):
    """
    Returns a virtual key name for a virtual key code code.
    E.g.: id_to_vkey(30) = "VK_1"

    :param code: virtual key code
    :return: virtual key name (VK_*)
    :rtype: str
    """
    if code == 0x88:
        return "VK_NRETURN"
    if code == 5:
        return "VK_XBUTTON1"
    if code == 6:
        return "VK_XBUTTON2"
    if (0x30 <= code <= 0x39) or (0x41 <= code <= 0x5A):
        return 'VK_' + chr(code)
    else:
        return pyHook.HookConstants.id_to_vk.get(code)
