# coding=utf-8

from Key import VirtualKey
import Hook

__author__ = 'Felix'

from Layout import Layer
from KeyMap import KeyMap


layer_2 = Layer()
layer_2.add_SimpleKey(VirtualKey("Q"), VirtualKey("PRIOR"))
layer_2.add_SimpleKey(VirtualKey("W"), VirtualKey("BACK"))
layer_2.add_SimpleKey(VirtualKey("E"), VirtualKey("UP"))
layer_2.add_SimpleKey(VirtualKey("R"), VirtualKey("DELETE"))
layer_2.add_SimpleKey(VirtualKey("T"), VirtualKey("NEXT"))

layer_2.add_SimpleKey(VirtualKey("A"), VirtualKey("HOME"))
layer_2.add_SimpleKey(VirtualKey("S"), VirtualKey("LEFT"))
layer_2.add_SimpleKey(VirtualKey("D"), VirtualKey("DOWN"))
layer_2.add_SimpleKey(VirtualKey("F"), VirtualKey("RIGHT"))
layer_2.add_SimpleKey(VirtualKey("G"), VirtualKey("END"))

layer_2.add_SimpleKey(VirtualKey("Y"), VirtualKey("ESCAPE"))
layer_2.add_SimpleKey(VirtualKey("X"), VirtualKey("TAB"))
layer_2.add_SimpleKey(VirtualKey("C"), VirtualKey("INSERT"))
layer_2.add_SimpleKey(VirtualKey("V"), VirtualKey("RETURN"))

layer_3 = Layer()

layer_3.add_SimpleUnicodeKey(VirtualKey("TAB"), "$")
layer_3.add_SimpleUnicodeKey(VirtualKey("Q"), "*")
layer_3.add_SimpleKey(VirtualKey("W"), VirtualKey("9"))
layer_3.add_SimpleKey(VirtualKey("E"), VirtualKey("8"))
layer_3.add_SimpleKey(VirtualKey("R"), VirtualKey("7"))
layer_3.add_SimpleUnicodeKey(VirtualKey("T"), "/")

layer_3.add_SimpleUnicodeKey(VirtualKey("VK_CAPITAL"), ".")
layer_3.add_SimpleKey(VirtualKey("A"), VirtualKey("0"))
layer_3.add_SimpleKey(VirtualKey("S"), VirtualKey("6"))
layer_3.add_SimpleKey(VirtualKey("D"), VirtualKey("5"))
layer_3.add_SimpleKey(VirtualKey("F"), VirtualKey("4"))
layer_3.add_SimpleUnicodeKey(VirtualKey("G"), ",")

layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_102"), 0x20AC)
layer_3.add_SimpleUnicodeKey(VirtualKey("Y"), "+")
layer_3.add_SimpleKey(VirtualKey("X"), VirtualKey("3"))
layer_3.add_SimpleKey(VirtualKey("C"), VirtualKey("2"))
layer_3.add_SimpleKey(VirtualKey("V"), VirtualKey("1"))
layer_3.add_SimpleUnicodeKey(VirtualKey("B"), "-")

# Right side:
layer_3.add_SimpleUnicodeKey(VirtualKey("Z"), "\\")
layer_3.add_SimpleUnicodeKey(VirtualKey("U"), "[")
layer_3.add_SimpleUnicodeKey(VirtualKey("I"), "]")
layer_3.add_SimpleUnicodeKey(VirtualKey("O"), "<")
layer_3.add_SimpleUnicodeKey(VirtualKey("P"), ">")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_1"), "@")

layer_3.add_SimpleUnicodeKey(VirtualKey("H"), "%")
layer_3.add_SimpleUnicodeKey(VirtualKey("J"), "(")
layer_3.add_SimpleUnicodeKey(VirtualKey("K"), ")")
layer_3.add_SimpleUnicodeKey(VirtualKey("L"), "{")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_3"), "}")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_7"), "#")

layer_3.add_SimpleUnicodeKey(VirtualKey("N"), "=")
layer_3.add_SimpleUnicodeKey(VirtualKey("M"), "!")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_COMMA"), "?")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_PERIOD"), "\"")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_OEM_MINUS"), "'")
layer_3.add_SimpleUnicodeKey(VirtualKey("VK_RSHIFT"), "^")

layer_3.add_SimpleKey(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_3.add_SimpleKey(VirtualKey("4"), VirtualKey("BACK"))
layer_3.add_SimpleKey(VirtualKey("5"), VirtualKey("RETURN"))

layer_3.add_SimpleKey(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_3.add_SimpleKey(VirtualKey("8"), VirtualKey("BACK"))
layer_3.add_SimpleKey(VirtualKey("7"), VirtualKey("RETURN"))

layer_4 = Layer()

layer_4.add_SimpleKey(VirtualKey("TAB"), VirtualKey("TAB"))
layer_4.add_SimpleKey(VirtualKey("Q"), VirtualKey("F12"))
layer_4.add_SimpleKey(VirtualKey("W"), VirtualKey("F11"))
layer_4.add_SimpleKey(VirtualKey("E"), VirtualKey("F10"))
layer_4.add_SimpleKey(VirtualKey("R"), VirtualKey("F9"))
layer_4.add_SimpleKey(VirtualKey("T"), VirtualKey("SCROLL"))

# layer_4.add_SimpleKey(VirtualKey("CAPITAL"), VirtualKey(""))
layer_4.add_SimpleKey(VirtualKey("A"), VirtualKey("F8"))
layer_4.add_SimpleKey(VirtualKey("S"), VirtualKey("F7"))
layer_4.add_SimpleKey(VirtualKey("D"), VirtualKey("F6"))
layer_4.add_SimpleKey(VirtualKey("F"), VirtualKey("F5"))
layer_4.add_SimpleKey(VirtualKey("G"), VirtualKey("SNAPSHOT"))

# layer_4.add_SimpleKey(VirtualKey("OEM_102"), VirtualKey(""))
layer_4.add_SimpleKey(VirtualKey("Y"), VirtualKey("F4"))
layer_4.add_SimpleKey(VirtualKey("X"), VirtualKey("F3"))
layer_4.add_SimpleKey(VirtualKey("C"), VirtualKey("F2"))
layer_4.add_SimpleKey(VirtualKey("V"), VirtualKey("F1"))
layer_4.add_SimpleKey(VirtualKey("B"), VirtualKey("PAUSE"))

# RIGHT
layer_4.add_SimpleKey(VirtualKey("Z"), VirtualKey("PRIOR"))
layer_4.add_SimpleKey(VirtualKey("U"), VirtualKey("BACK"))
layer_4.add_SimpleKey(VirtualKey("I"), VirtualKey("UP"))
layer_4.add_SimpleKey(VirtualKey("O"), VirtualKey("DELETE"))
layer_4.add_SimpleKey(VirtualKey("P"), VirtualKey("NEXT"))

layer_4.add_SimpleKey(VirtualKey("H"), VirtualKey("HOME"))
layer_4.add_SimpleKey(VirtualKey("J"), VirtualKey("LEFT"))
layer_4.add_SimpleKey(VirtualKey("K"), VirtualKey("DOWN"))
layer_4.add_SimpleKey(VirtualKey("L"), VirtualKey("RIGHT"))
layer_4.add_SimpleKey(VirtualKey("OEM_3"), VirtualKey("END"))

layer_4.add_SimpleKey(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_4.add_SimpleKey(VirtualKey("4"), VirtualKey("BACK"))
layer_4.add_SimpleKey(VirtualKey("5"), VirtualKey("RETURN"))

layer_4.add_SimpleKey(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_4.add_SimpleKey(VirtualKey("8"), VirtualKey("BACK"))
layer_4.add_SimpleKey(VirtualKey("7"), VirtualKey("RETURN"))

layer_1 = Layer()
layer_1.add_default_keys()

layer_1.add_SimpleKey(VirtualKey("3"), VirtualKey("ESCAPE"))
layer_1.add_SimpleKey(VirtualKey("4"), VirtualKey("BACK"))
layer_1.add_SimpleKey(VirtualKey("5"), VirtualKey("RETURN"))

layer_1.add_SimpleKey(VirtualKey("9"), VirtualKey("ESCAPE"))
layer_1.add_SimpleKey(VirtualKey("8"), VirtualKey("BACK"))
layer_1.add_SimpleKey(VirtualKey("7"), VirtualKey("RETURN"))
layer_1.add_SimpleUnicodeKey(VirtualKey("CAPITAL"), 0x00DF)

layer_1.add_ComplexKey(VirtualKey("SPACE"), VirtualKey("SPACE"), layer_3)
layer_1.add_SimpleMod(VirtualKey("OEM_102"), layer_4)
layer_1.add_SimpleMod(VirtualKey("OEM_MINUS"), layer_4)

layer_1.add_SimpleKey(VirtualKey("NRETURN"), VirtualKey("NRETURN"))

def_layer = Layer()
def_layer.add_default_keys()
# def_layer.add_SimpleUnicodeKey(VirtualKey("F"), "?")

key_map = KeyMap(layer_1)

Hook.create_hook(key_map.process_keystroke)
Hook.pump_messages(key_map.update, 0.001)
