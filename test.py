# coding=utf-8

from Key import VirtualKey
from SysTrayIcon import SysTrayIcon

__author__ = 'Felix'

from Layout import Layer
from KeyMap import KeyMap

import logging

logging.basicConfig(level=logging.INFO)


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

layer_1 = Layer('layer_1')
layer_1.add_default_keys()

layer_1.add_complex_key(VirtualKey("SPACE"), VirtualKey("SPACE"), layer_3)

layer_1.add_simple_key(VirtualKey("NRETURN"), VirtualKey("NRETURN"))

key_map = KeyMap(layer_1, VirtualKey('SCROLL'))


def close(sysTrayIcon):
    key_map.in_out_adapter.hook.exit_event.set()


def do_nothing(sysTrayIcon):
    print("test")


menu_options = (('Pause', None, do_nothing),
                ('A sub-menu', None, (('Option 1', None, do_nothing),
                                      ('Option 2', None, do_nothing),)))

sti = SysTrayIcon('resources/keyboard.ico', 'KeyFun', menu_options, on_quit=close)
print("start")
key_map.in_out_adapter.run_hooks(key_map.update, 0.001)
