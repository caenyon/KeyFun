# coding=utf-8

from Key import VirtualKey

__author__ = 'Felix'

from Layout import Layer
from KeyMap import KeyMap

import logging
logging.basicConfig(level=logging.DEBUG)


layer_2 = Layer('layer_2')
layer_2.add_simple_key(VirtualKey("Q"), VirtualKey("PRIOR"))
layer_2.add_simple_key(VirtualKey("W"), VirtualKey("BACK"))
layer_2.add_simple_key(VirtualKey("E"), VirtualKey("UP"))
layer_2.add_simple_key(VirtualKey("R"), VirtualKey("DELETE"))
layer_2.add_simple_key(VirtualKey("T"), VirtualKey("NEXT"))

layer_2.add_simple_key(VirtualKey("A"), VirtualKey("HOME"))
layer_2.add_simple_key(VirtualKey("S"), VirtualKey("LEFT"))
layer_2.add_simple_key(VirtualKey("D"), VirtualKey("DOWN"))
layer_2.add_simple_key(VirtualKey("F"), VirtualKey("RIGHT"))
layer_2.add_simple_key(VirtualKey("G"), VirtualKey("END"))

layer_2.add_simple_key(VirtualKey("Y"), VirtualKey("ESCAPE"))
layer_2.add_simple_key(VirtualKey("X"), VirtualKey("TAB"))
layer_2.add_simple_key(VirtualKey("C"), VirtualKey("INSERT"))
layer_2.add_simple_key(VirtualKey("V"), VirtualKey("RETURN"))

layer_3 = Layer('layer_3')

layer_3.add_simple_unicode_key(VirtualKey("TAB"), "$")
layer_3.add_simple_unicode_key(VirtualKey("Q"), "*")
layer_3.add_simple_key(VirtualKey("W"), VirtualKey("9"))
layer_3.add_simple_key(VirtualKey("E"), VirtualKey("8"))
layer_3.add_simple_key(VirtualKey("R"), VirtualKey("7"))
layer_3.add_simple_unicode_key(VirtualKey("T"), "/")

layer_3.add_simple_unicode_key(VirtualKey("VK_CAPITAL"), ".")
layer_3.add_simple_key(VirtualKey("A"), VirtualKey("0"))
layer_3.add_simple_key(VirtualKey("S"), VirtualKey("6"))
layer_3.add_simple_key(VirtualKey("D"), VirtualKey("5"))
layer_3.add_simple_key(VirtualKey("F"), VirtualKey("4"))
layer_3.add_simple_unicode_key(VirtualKey("G"), ",")

layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_102"), 0x20AC)
layer_3.add_simple_unicode_key(VirtualKey("Y"), "+")
layer_3.add_simple_key(VirtualKey("X"), VirtualKey("3"))
layer_3.add_simple_key(VirtualKey("C"), VirtualKey("2"))
layer_3.add_simple_key(VirtualKey("V"), VirtualKey("1"))
layer_3.add_simple_unicode_key(VirtualKey("B"), "-")

# Right side:
layer_3.add_simple_unicode_key(VirtualKey("Z"), "\\")
layer_3.add_simple_unicode_key(VirtualKey("U"), "[")
layer_3.add_simple_unicode_key(VirtualKey("I"), "]")
layer_3.add_simple_unicode_key(VirtualKey("O"), "<")
layer_3.add_simple_unicode_key(VirtualKey("P"), ">")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_1"), "@")

layer_3.add_simple_unicode_key(VirtualKey("H"), "%")
layer_3.add_simple_unicode_key(VirtualKey("J"), "(")
layer_3.add_simple_unicode_key(VirtualKey("K"), ")")
layer_3.add_simple_unicode_key(VirtualKey("L"), "{")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_3"), "}")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_7"), "#")

layer_3.add_simple_unicode_key(VirtualKey("N"), "=")
layer_3.add_simple_unicode_key(VirtualKey("M"), "!")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_COMMA"), "?")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_PERIOD"), "\"")
layer_3.add_simple_unicode_key(VirtualKey("VK_OEM_MINUS"), "'")
layer_3.add_simple_unicode_key(VirtualKey("VK_RSHIFT"), "^")

layer_3.add_simple_key(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_3.add_simple_key(VirtualKey("4"), VirtualKey("BACK"))
layer_3.add_simple_key(VirtualKey("5"), VirtualKey("RETURN"))

layer_3.add_simple_key(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_3.add_simple_key(VirtualKey("8"), VirtualKey("BACK"))
layer_3.add_simple_key(VirtualKey("7"), VirtualKey("RETURN"))

layer_4 = Layer('layer_4')

layer_4.add_simple_key(VirtualKey("TAB"), VirtualKey("TAB"))
layer_4.add_simple_key(VirtualKey("Q"), VirtualKey("F12"))
layer_4.add_simple_key(VirtualKey("W"), VirtualKey("F11"))
layer_4.add_simple_key(VirtualKey("E"), VirtualKey("F10"))
layer_4.add_simple_key(VirtualKey("R"), VirtualKey("F9"))
layer_4.add_simple_key(VirtualKey("T"), VirtualKey("SCROLL"))

# layer_4.add_simple_key(VirtualKey("CAPITAL"), VirtualKey(""))
layer_4.add_simple_key(VirtualKey("A"), VirtualKey("F8"))
layer_4.add_simple_key(VirtualKey("S"), VirtualKey("F7"))
layer_4.add_simple_key(VirtualKey("D"), VirtualKey("F6"))
layer_4.add_simple_key(VirtualKey("F"), VirtualKey("F5"))
layer_4.add_simple_key(VirtualKey("G"), VirtualKey("SNAPSHOT"))

# layer_4.add_simple_key(VirtualKey("OEM_102"), VirtualKey(""))
layer_4.add_simple_key(VirtualKey("Y"), VirtualKey("F4"))
layer_4.add_simple_key(VirtualKey("X"), VirtualKey("F3"))
layer_4.add_simple_key(VirtualKey("C"), VirtualKey("F2"))
layer_4.add_simple_key(VirtualKey("V"), VirtualKey("F1"))
layer_4.add_simple_key(VirtualKey("B"), VirtualKey("PAUSE"))

# RIGHT
layer_4.add_simple_key(VirtualKey("Z"), VirtualKey("PRIOR"))
layer_4.add_simple_key(VirtualKey("U"), VirtualKey("BACK"))
layer_4.add_simple_key(VirtualKey("I"), VirtualKey("UP"))
layer_4.add_simple_key(VirtualKey("O"), VirtualKey("DELETE"))
layer_4.add_simple_key(VirtualKey("P"), VirtualKey("NEXT"))

layer_4.add_simple_key(VirtualKey("H"), VirtualKey("HOME"))
layer_4.add_simple_key(VirtualKey("J"), VirtualKey("LEFT"))
layer_4.add_simple_key(VirtualKey("K"), VirtualKey("DOWN"))
layer_4.add_simple_key(VirtualKey("L"), VirtualKey("RIGHT"))
layer_4.add_simple_key(VirtualKey("OEM_3"), VirtualKey("END"))

layer_4.add_simple_key(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_4.add_simple_key(VirtualKey("4"), VirtualKey("BACK"))
layer_4.add_simple_key(VirtualKey("5"), VirtualKey("RETURN"))

layer_4.add_simple_key(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_4.add_simple_key(VirtualKey("8"), VirtualKey("BACK"))
layer_4.add_simple_key(VirtualKey("7"), VirtualKey("RETURN"))

layer_1 = Layer('layer_1')
layer_1.add_default_keys()

layer_1.add_simple_key(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_1.add_simple_key(VirtualKey("4"), VirtualKey("BACK"))
layer_1.add_simple_key(VirtualKey("5"), VirtualKey("RETURN"))

layer_1.add_simple_key(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_1.add_simple_key(VirtualKey("8"), VirtualKey("BACK"))
layer_1.add_simple_key(VirtualKey("7"), VirtualKey("RETURN"))
layer_1.add_simple_unicode_key(VirtualKey("CAPITAL"), 0x00DF)

layer_1.add_complex_key(VirtualKey("SPACE"), VirtualKey("SPACE"), layer_3)
layer_1.add_simple_mod(VirtualKey("OEM_102"), layer_4)
# layer_1.add_simple_mod(VirtualKey("OEM_MINUS"), layer_4)

layer_1.add_simple_key(VirtualKey("NRETURN"), VirtualKey("NRETURN"))

def_layer = Layer('layer_def')
def_layer.add_default_keys()
# def_layer.add_simple_unicode_key(VirtualKey("F"), "?")

key_map = KeyMap(layer_1, VirtualKey('SCROLL'))

key_map.in_out_adapter.run_hooks(key_map.update, 0.001)
