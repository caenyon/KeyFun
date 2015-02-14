import time

import pyHook
import pythoncom

import Constants
from Key import VirtualKey


__author__ = 'Felix'

triggered_keys = []
process_keystroke = None
physically_pressed_keys = set()
hook_manager = None


def create_hook(process_keystroke_func):
    """
    Creates a keyboard hook.
    """
    global process_keystroke, hook_manager
    process_keystroke = process_keystroke_func
    hook_manager = pyHook.HookManager()
    hook_manager.KeyAll = handle_keyboard_all
    hook_manager.HookKeyboard()
    # Create Hook for mouse manually, because the pyHook-Version does not support XBUTTONS
    pyHook.cpyHook.cSetHook(pyHook.HookConstants.WH_MOUSE_LL, mouse_handler)
    # TODO close hooks on exit...


def pump_messages(update, pump_messages_delay):
    """
    Pumps messages until Hook.exit_flag is set.
    """

    while True:
        update()
        pythoncom.PumpWaitingMessages()
        time.sleep(pump_messages_delay)


def mouse_handler(msg, _x, _y, data, _flags, _time, _hwnd, _window_name):
    # Check if the msg is known
    try:
        name = Constants.mouse_codes[msg]
    except:
        raise Exception("Unknown Mouse Event: Msg={}".format(hex(msg)))

    if name == "WM_MOUSEMOVE":
        # Mouse was moved. This should not be filtered
        return True

    if name == "WM_MOUSEWHEEL" or name == "WM_MOUSEHWHEEL":
        # Mouse wheel / horizontal wheel was moved.
        # Should not be filtered
        return True

    assert name[-2:] == "UP" or name[-4:] == "DOWN"
    key_down = (name[-4:] == "DOWN")
    relevant_data = data >> 16

    key_name = name[3]
    if key_name == "L":
        mouse_event_id = 0x01
    elif key_name == "R":
        mouse_event_id = 0x02
    elif key_name == "M":
        mouse_event_id = 0x04
    elif key_name == "X":
        if relevant_data & 0x0001 > 0:
            # XBUTTON1 event
            mouse_event_id = 0x05
        elif relevant_data & 0x0002 > 0:
            # XBUTTON2 event
            mouse_event_id = 0x06
        else:
            raise Exception("Unknown XBUTTON event: Name={1}, Data={2}".format(name, relevant_data))
    else:
        raise Exception("Bad mouse event name: {}".format(name))

    return filter_dublicates(mouse_event_id, key_down)


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

    virtual_key = VirtualKey(event.KeyID)
    print "-------", str(virtual_key), event.KeyID, event.IsExtended(), event.IsTransition()
    # return True

    # this is the left control key that is sent with the right Alt key
    if event.KeyID == 162 and event.ScanCode == 541:
        return False

    # this is the numpad return key
    if event.KeyID == 0x0D and event.IsExtended():
        print("NUMPAD ENTER")
        event.KeyID = 0x88

    if event.KeyID == 0xE7:
        return True

    return filter_dublicates(event.KeyID, key_down)


def filter_dublicates(vKey_id, key_down):
    # check if the received key event was triggered by the program
    if (vKey_id, key_down) in triggered_keys:
        triggered_keys.remove((vKey_id, key_down))
        return True
    else:
        if key_down and vKey_id not in physically_pressed_keys:
            # Key pressed event
            physically_pressed_keys.add(vKey_id)

            process_keystroke(vKey_id, key_down)

        elif not key_down and vKey_id in physically_pressed_keys:
            # Key released event
            physically_pressed_keys.remove(vKey_id)

            process_keystroke(vKey_id, key_down)

        return False
