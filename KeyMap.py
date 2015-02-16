import time
import logging

import Constants
from InOut.InOutAdapter import InOutAdapter
from Key import SimpleKey, SimpleModifier, ComplexKey, SimpleUnicodeKey


__author__ = 'Felix'

pressed_keys = set()
in_out_adapter = InOutAdapter()


def press_key(key_id):
    pressed_keys.add(key_id)
    return in_out_adapter.send_key(key_id, True)


def release_key(key_id):
    pressed_keys.remove(key_id)
    return in_out_adapter.send_key(key_id, False)


def release_unicode_key(unicode_id):
    return in_out_adapter.send_unicode_key(unicode_id, False)


def press_unicode_key(unicode_id):
    return in_out_adapter.send_unicode_key(unicode_id, True)


def type_key(key_id):
    print('---Typed {}'.format(key_id))
    press_key(key_id)
    release_key(key_id)


def repress_key(key_id):
    if key_id not in (1, 2, 4, 5, 6, 91):
        # Mouse keys and left win key should not be repeated...
        return in_out_adapter.send_key(key_id, True)


# TODO: implement repress of unicode-keys


# noinspection PyMethodMayBeStatic
class KeyMap(object):
    def __init__(self, init_layer):
        self.init_layer = init_layer
        self.layer = init_layer
        self.delayed_keys = []
        self.ignore_key_release = set()
        self.physically_pressed_keys = {}
        self.pressed_time = {}
        self.long_press_delay = .3
        self.key_repeat_delay = 0.03
        self.key_init_repeat_delay = 0.2
        self.last_pressed = {}

    def process_keystroke(self, vkey_id, key_down):
        print('---{}-----------{}-----------------------------------------'.format(Constants.id_to_vkey(vkey_id),
                                                                                   key_down))
        # if the key had been released because of a layer change, the corresponding physical key release should be
        # ignored.
        if not key_down and vkey_id in self.ignore_key_release:
            self.ignore_key_release.remove(vkey_id)
            print('ignore')
            return

        # are there keys in self.delayed_keys? if yes, there is a ComplexKey at self.delayed_keys[0] and its not
        # clear if this key is used as a modifier or as a key
        if len(self.delayed_keys) > 0:
            print('delayed keys!')
            if key_down:
                # when a key is pressed in this state, its action is not clear and it must be delayed until the layer
                # is clear
                self.delayed_keys.append(vkey_id)
                self.pressed_time[vkey_id] = time.time()  # TODO: Reduce memory usage...
                return
            else:
                # a key was released. This can have one of the following meanings:
                # 1. the ComplexKey that is the first item of self.delayed_keys has been released
                if self.delayed_keys[0] == vkey_id:
                    print('case 1')
                    # this means that the ComplexKey was used as a key and not as a modifier
                    action = self.layer[vkey_id]

                    # type the key associated with the ComplexKey
                    type_key(int(action.vKeyName))
                    # TODO: what about unicode here?

                    # remove the ComplexKey from the list of delayed_keys
                    self.delayed_keys.pop(0)

                    # release other keys in self.delayed_keys
                    self.release_delayed_keys()

                # 2. a key in self.delayed_keys has been released
                elif vkey_id in self.delayed_keys:
                    print('case 2')
                    # this means that the ComplexKey is used as a modifier

                    # change the layer
                    self.set_layer(self.layer[self.delayed_keys[0]].newLayer)

                    # remove ComplexKey from self.delayed_keys
                    self.delayed_keys.pop(0)

                    # release other keys in self.delayed_keys
                    self.release_delayed_keys()

                    # status changed, redo key event
                    self.process_keystroke(vkey_id, key_down)

                # 3. released key is not in delayed_keys. this means that the key had been pressed before the first
                # ComplexKey in delayed_keys was pressed.
                else:
                    print('case 3')
                    # simply release that key

                    # this key can be a SimpleKey, a SimpleModifier or a ComplexKey which is used as a modifier.

                    # in case of a SimpleKey, the action is released and no changes are done to the layer.
                    # in case of a SimpleMod or ComplexKey, the layer is set to the initial Layer and all physically
                    # pressed key are appended to the ignore release list. additionally all pressed SimpleKeys are
                    # released.

                    # get the action for that key press
                    action = self.physically_pressed_keys[vkey_id]

                    if isinstance(action, SimpleKey):
                        del self.physically_pressed_keys[int(action.vKeyName)]
                        release_key(int(action.vKeyName))
                    elif isinstance(action, SimpleUnicodeKey):
                        del self.physically_pressed_keys[int(action.id)]
                        release_unicode_key(action.id)
                    else:
                        self.release_layer()
            return

        # key is not defined in the current layer
        if (vkey_id not in self.layer and key_down) or (vkey_id not in self.physically_pressed_keys and not key_down):
            print('undefined Keystroke {}'.format(Constants.id_to_vkey(vkey_id)))
            return

        # bei released die action aus self.physically_pressed_keys nehmen
        action = self.layer[vkey_id]
        if not key_down:
            action = self.physically_pressed_keys[vkey_id]

        if key_down:
            self.physically_pressed_keys[vkey_id] = action
        else:

            del self.physically_pressed_keys[vkey_id]

        # print('performing action')
        if isinstance(action, SimpleKey):
            self.process_simple_key(action, key_down)
        elif isinstance(action, SimpleUnicodeKey):
            self.process_simple_unicode_key(action, key_down)
        elif isinstance(action, SimpleModifier):
            self.process_simple_mod(action, key_down)
        elif isinstance(action, ComplexKey):
            self.process_complex_key(action, key_down)

    def release_delayed_keys(self):

        while True:
            if len(self.delayed_keys) == 0:
                break

            key = self.delayed_keys[0]
            action = self.layer[key]

            if isinstance(action, ComplexKey):
                break
            elif isinstance(action, SimpleKey):
                self.physically_pressed_keys[key] = action
                self.process_simple_key(action, True)
            elif isinstance(action, SimpleUnicodeKey):
                self.physically_pressed_keys[key] = action
                self.process_simple_unicode_key(action, True)
            elif isinstance(action, SimpleModifier):
                self.physically_pressed_keys[key] = action
                self.process_simple_mod(action, True)
            self.delayed_keys.pop(0)

    def set_layer(self, new_layer):
        logging.info('New Layer: '+new_layer.name)
        self.layer = new_layer

    def release_layer(self):
        for key in self.physically_pressed_keys:
            action = self.physically_pressed_keys[key]
            if isinstance(action, SimpleKey):
                release_key(int(action.vKeyName))
                # TODO What about unicode here
            self.ignore_key_release.add(key)
        self.physically_pressed_keys = {}
        self.layer = self.init_layer
        logging.info('New Layer: '+self.init_layer.name)

    def process_simple_key(self, action, key_down):
        if key_down:
            # print('Key {} down'.format(action.vKeyName))
            press_key(int(action.vKeyName))
        else:
            # print('Key {} up'.format(action.vKeyName))
            release_key(int(action.vKeyName))

    def process_simple_unicode_key(self, action, key_down):
        if key_down:
            # print('UnicodeKey {} down'.format(action.id))
            press_unicode_key(action.id)
        else:
            # print('UnicodeKey {} up'.format(action.id))
            release_unicode_key(action.id)

    def process_simple_mod(self, action, key_down):
        if key_down:
            self.set_layer(action.newLayer)
        else:
            self.release_layer()

    def process_complex_key(self, action, key_down):
        if key_down:
            self.pressed_time[int(action.vKeyName)] = time.time()
            self.delayed_keys.append(int(action.vKeyName))
        else:
            self.release_layer()

    def update(self):
        # make long pressed complexKeys modifiers
        if len(self.delayed_keys) > 0:
            if (time.time() - self.pressed_time[self.delayed_keys[0]]) > self.long_press_delay:
                # change the layer
                self.set_layer(self.layer[self.delayed_keys[0]].newLayer)

                # remove ComplexKey from self.delayed_keys
                self.delayed_keys.pop(0)

                # release other keys in self.delayed_keys
                self.release_delayed_keys()

                print "long press!"

        pressed = frozenset(pressed_keys)
        all_pressed = set()
        all_pressed = all_pressed.union(pressed)
        for key in self.last_pressed:
            all_pressed.add(key)

        for key in all_pressed:
            if key in pressed and key not in self.last_pressed:
                self.last_pressed[key] = time.time() + self.key_init_repeat_delay
            elif key in pressed and key in self.last_pressed:
                if time.time() - self.last_pressed[key] > self.key_repeat_delay:
                    repress_key(key)
                    self.last_pressed[key] = time.time()
            elif key not in pressed and key in self.last_pressed:
                del self.last_pressed[key]
