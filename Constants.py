# -*- coding: utf-8 -*-
"""
Constants contains several functions and constants useful in other modules.
"""
__author__ = 'Felix'

import pyHook


def generate_key_id_name_mappings():
    name_to_id = {}

    # copy mapping contained in pyHook
    for key in pyHook.HookConstants.vk_to_id:
        name_to_id[key] = pyHook.HookConstants.vk_to_id[key]

    # add entries for numbers and letters
    for i in range(0x41, 0x5A + 1) + range(0x30, 0x39 + 1):
        name_to_id['VK_' + chr(i)] = i

    # append XBUTTONs and Numpad return key
    name_to_id['VK_XBUTTON1'] = 0x05
    name_to_id['VK_XBUTTON2'] = 0x06
    name_to_id['VK_NRETURN'] = 0x88

    # invert the mapping
    id_to_name = dict([(v, k) for k, v in name_to_id.items()])

    return name_to_id, id_to_name

# generate the bindings from key names to key ids and from key ids to key names.
key_name_to_id, key_id_to_name = generate_key_id_name_mappings()
