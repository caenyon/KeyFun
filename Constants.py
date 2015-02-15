# -*- coding: utf-8 -*-
"""
Constants contains several functions and constants useful in other modules.
"""
__author__ = 'Felix'

import pyHook

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
