# -*- coding: utf-8 -*-
"""
Module Hook

Contains class Hook.
"""
import Queue
import threading
import time
import logging

import pyHook
import pythoncom

import Constants
import Send


class Hook(object):
    """
    Static class holding code for keyboard hook management.
    """

    simulated_keys = Queue.Queue()
    scroll_grid_size = 10
    shift_down = False
    last_pressed = {}
    virtually_pressed_keys = []
    delayed_keys = {}
    modded_keys = []
    mod = []
    mod_cand = {}
    pump_messages_delay = 0.001
    max_key_press_duration = .3
    hook_manager = None
    exit_flag = threading.Event()
    pause_flag = threading.Event()
    physically_pressed_keys = set()
    highlight_keys = Queue.Queue()
    reset_highlight_keys = Queue.Queue()
    triggered_keys = []
    logically_pressed_keys = {}
    key_repeat_delay = 0.03
    key_init_repeat_delay = 0.2
    key_init_repeat_delay -= key_repeat_delay
    sync = threading.Event()

    key_pressed_time = {}
    times = []

    v_scroll = 0
    mouse_pos = (0, 0)

    def __init__(self):
        pass

    @staticmethod
    def handle_mouse_all(event):
        """

        :param event:
        :type event: pyHook.MouseEvent
        :return:
        :rtype:
        """


        if len(Hook.mod) + len(Hook.mod_cand) > 0 and event.MessageName == 'mouse move':
            Send.scroll((event.Position[1] - Hook.mouse_pos[1])*-16)

            return False

            #print Hook.v_scroll

            while abs(Hook.v_scroll) > Hook.scroll_grid_size:
                if Hook.v_scroll < 0:

                    Hook.triggered_keys.append((Constants.vk_to_id["VK_UP"], True))
                    Send.press_key(Constants.vk_to_id["VK_UP"])
                    Hook.triggered_keys.append((Constants.vk_to_id["VK_UP"], False))
                    Send.release_key(Constants.vk_to_id["VK_UP"])
                    Hook.v_scroll += Hook.scroll_grid_size
                elif Hook.v_scroll > 0:
                    Hook.triggered_keys.append((Constants.vk_to_id["VK_DOWN"], True))
                    Send.press_key(Constants.vk_to_id["VK_DOWN"])
                    Hook.triggered_keys.append((Constants.vk_to_id["VK_DOWN"], False))
                    Send.release_key(Constants.vk_to_id["VK_DOWN"])
                    Hook.v_scroll -= Hook.scroll_grid_size


            return False

        Hook.mouse_pos = event.Position
        return True

    @staticmethod
    def handle_keyboard_all(event):
        """
        Method that processes keyboard events sent by pyHook.

        :param event: the event to process
        :type event: pyHook.KeyboardEvent
        :return: boolean flag indicating if the event should be passed to the next handler
        :rtype: bool
        """

        # key_down = 1: Key pressed
        # key_down = 0: Key released
        key_down = (event.IsTransition() == 0)

        # this is the left control key that is sent with the right Alt key
        if event.KeyID == 162 and event.ScanCode == 541:
            return False

        # this is the numpad return key
        if event.KeyID == 0x0D and event.IsExtended():
            event.KeyID = 1000

        # check if the received key event was triggered by the program
        if (event.KeyID, key_down) in Hook.triggered_keys:
            Hook.triggered_keys.remove((event.KeyID, key_down))

            Hook.simulated_keys.put((event.KeyID, key_down))
            return True
        else:
            if key_down and not event.KeyID in Hook.physically_pressed_keys:
                # Key pressed event
                Hook.physically_pressed_keys.add(event.KeyID)
                Hook.key_pressed_time[event.KeyID] = event.Time
                Hook.highlight_keys.put(event.KeyID)

                # print("{} down".format(Constants.id_to_vkey(event.KeyID)))
                if Hook.key_filter(event.KeyID):
                    Hook.process_event(event)
                else:
                    return True

            elif not key_down and event.KeyID in Hook.physically_pressed_keys:
                # Key released event
                Hook.physically_pressed_keys.remove(event.KeyID)
                Hook.reset_highlight_keys.put(event.KeyID)

                duration = (event.Time - Hook.key_pressed_time[event.KeyID]) / 1000.0
                Hook.times.append(duration)
                # print("{} up after {}s".format(Constants.id_to_vkey(event.KeyID), duration))
                if Hook.key_filter(event.KeyID):
                    Hook.process_event(event)
                else:
                    return True
            return False

    @staticmethod
    def key_filter(key_id):
        # filter, only letters and space
        if not (0x41 <= key_id <= 0x5A) and not key_id == 0x20:
            return False
        return True

    @staticmethod
    def process_event(event):
        key_down = (event.IsTransition() == 0)
        #print('+Event: {} {}'.format('down' if key_down else 'up', Constants.id_to_vkey(event.KeyID)))

        # check if pressed or released key is ComplexKey
        if Constants.id_to_vkey(event.KeyID) == 'VK_SPACE':
            if key_down:

                # ComplexKey pressed
                Hook.mod_cand[event.KeyID] = time.time()
            else:

                # ComplexKey released

                if event.KeyID in Hook.mod_cand:
                    del Hook.mod_cand[event.KeyID]


                    # ComplexKey should be used as normal Key
                    Hook.sendKey(event.KeyID, True)
                    Hook.sendKey(event.KeyID, False)

                    # delete modifier candidate from all delayed keys
                    Hook.release_delayes_keys(event.KeyID, False)

                else:
                    # ComplexKey should be used as a modifier
                    Hook.mod.remove(event.KeyID)
        else:

            if key_down:
                # Normal key pressed

                if len(Hook.mod_cand) > 0:
                    # delay key until modifier candidates are cleared
                    mod_candidates = [key for key in Hook.mod_cand]
                    Hook.delayed_keys[event.KeyID] = (tuple(Hook.mod), mod_candidates)
                else:
                    # send key with the modifiers set at the moment
                    mod = None if len(Hook.mod) == 0 else 2
                    Hook.sendKey(event.KeyID, True, mod)
            else:
                # Normal key released

                if event.KeyID in Hook.delayed_keys:
                    # Key was delayed because of modifier candidates
                    delete_candidates = []
                    for key in Hook.delayed_keys[event.KeyID][1]:
                        delete_candidates.append(key)
                    for key in delete_candidates:
                        Hook.candidate_to_modifier(key)

                # if the key was delayed or not, it should be released now.
                Hook.sendKey(event.KeyID, False)
        Hook.print_status()

    @staticmethod
    def check_long_press():

        deleteList = []
        for key in Hook.mod_cand:
            if time.time() - Hook.mod_cand[key] > Hook.max_key_press_duration:
                deleteList.append(key)

        for key in deleteList:
            #print('+Event: Long press {}'.format(Constants.id_to_vkey(key)))
            Hook.candidate_to_modifier(key)
            Hook.print_status()

    @staticmethod
    def candidate_to_modifier(vkey_id):
        del Hook.mod_cand[vkey_id]
        Hook.mod.append(vkey_id)

        Hook.release_delayes_keys(vkey_id, True)

    @staticmethod
    def release_delayes_keys(vkey_mod_cand, make_modifier):
        to_delete_keys = []
        for key in Hook.delayed_keys:
            mod, mod_cand = Hook.delayed_keys[key]
            if not vkey_mod_cand in mod_cand:
                continue

            if make_modifier:
                mod = list(mod)
                mod.append(vkey_mod_cand)

            if len(mod_cand) == 1:
                # only one candidate key that is the key that has to be transformed to a modifier
                # release key
                to_delete_keys.append(key)

                mod = None if len(mod) == 0 else 'Modded'
                Hook.sendKey(key, True, mod)
            else:
                Hook.delayed_keys[key] = (mod, list(mod_cand).remove(key))

        for key in to_delete_keys:
            del Hook.delayed_keys[key]

    @staticmethod
    def retype_pressed_keys():
        all_keys = set()
        for key in Hook.virtually_pressed_keys:
            all_keys.add(key)
        for key in Hook.last_pressed:
            all_keys.add(key)
        for key in all_keys:
            if key in Hook.virtually_pressed_keys:
                if key in Hook.last_pressed:
                    # key is pressed and has got entry in last_pressed.
                    # check if retype
                    if time.time() - Hook.last_pressed[key] > Hook.key_repeat_delay:
                        Hook.triggered_keys.append((key, True))
                        Send.press_key(key)

                        Hook.last_pressed[key] = time.time()
                    pass
                else:
                    Hook.last_pressed[key] = time.time() + Hook.key_init_repeat_delay
            else:
                if key in Hook.last_pressed:
                    del Hook.last_pressed[key]
                else:
                    assert False


    @staticmethod
    def sendKey(vkey_id, key_down, mod=None):

        if mod is not None:
            if vkey_id in Constants.simpleMod and key_down:
                Hook.modded_keys.append(vkey_id)
                vkey_id = Constants.simpleMod[vkey_id]
        if not key_down and vkey_id in Hook.modded_keys:
            Hook.modded_keys.remove(vkey_id)
            vkey_id = Constants.simpleMod[vkey_id]
        #print('------Action: {} {} {}'.format('MOD' if mod is not None else '', Constants.id_to_vkey(vkey_id), \
        #                                'down' if key_down else 'up'))


        Hook.triggered_keys.append((vkey_id, key_down))
        if key_down:
            Send.press_key(vkey_id)

            Hook.virtually_pressed_keys.append(vkey_id)
        else:
            Send.release_key(vkey_id)

            Hook.virtually_pressed_keys.remove(vkey_id)

    @staticmethod
    def create_hook(event_all):
        """
        Creates a keyboard hook.

        :param event_all: function(func: pyHook.KeyboardEvent): bool
        """
        Hook.hook_manager = pyHook.HookManager()
        Hook.hook_manager.KeyAll = event_all
        Hook.hook_manager.MouseAll = Hook.handle_mouse_all
        Hook.hook_manager.HookKeyboard()
        #Hook.hook_manager.HookMouse()

    @staticmethod
    def delete_hook():
        """
        Unhooks the Keyboard and displays keypress statistics.
        """
        Hook.hook_manager.UnhookKeyboard()

        #print(sum(Hook.times) / len(Hook.times), max(Hook.times), min(Hook.times))

    @staticmethod
    def pump_non_blocking():
        """
        Pumps messages until Hook.exit_flag is set.
        """

        while not Hook.exit_flag.isSet():

            if Hook.pause_flag.isSet():
                Hook.pause()

            Hook.check_long_press()
            Hook.retype_pressed_keys()
            pythoncom.PumpWaitingMessages()
            time.sleep(Hook.pump_messages_delay)

    @staticmethod
    def pause():
        """
        Unhooks the keyboard and waits until Hook.pause_flag is cleared or Hook.exit_flag is set.
        """
        print("Pause")
        Hook.hook_manager.UnhookKeyboard()
        while Hook.pause_flag.is_set() and not Hook.exit_flag.is_set():
            time.sleep(.1)
        Hook.hook_manager.HookKeyboard()
        print("Continue")

    @staticmethod
    def run():
        """
        Initializes and starts a keyboard hook.
        """
        # noinspection PyBroadException
        try:
            Hook.exit_flag.clear()

            Hook.create_hook(Hook.handle_keyboard_all)
            logging.debug('Hook-Thread started')

            Hook.pump_non_blocking()

            Hook.delete_hook()
            logging.debug('Hook-Thread ended')
        except:
            logging.exception("General Exception in HookThread")

    @staticmethod
    def print_status():
        # print('--Status')
        # print('-Modifiers: {}'.format(Hook.mod))
        # print('-Candidates: {}'.format(Hook.mod_cand))
        # print('-Delayed Keys: {}'.format(Hook.delayed_keys))
        pass
