from Key import SimpleKey, VirtualKey
import Hook

__author__ = 'Felix'

from Layout import Layer
from KeyMap import KeyMap


def event_all(event):
    key_down = (event.IsTransition() == 0)
    map.process_keystroke(event.KeyID, key_down)
    return False

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


layer_1 = Layer()
layer_1.add_default_keys()
#layer_1.add_SimpleKey(VirtualKey("LSHIFT"), VirtualKey("SHIFT"))
#layer_1.add_SimpleKey(VirtualKey("RSHIFT"), VirtualKey("SHIFT"))
layer_1.add_ComplexKey(VirtualKey("SPACE"), VirtualKey("SPACE"), layer_2)

def_layer = Layer()
def_layer.add_default_keys()

map = KeyMap(layer_1)

Hook.create_hook(map.process_keystroke)
Hook.pump_messages(map.update, 0.001)
