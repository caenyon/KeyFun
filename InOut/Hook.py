import time
import threading

import pyHook
import pythoncom


MOUSE_CODES = {0x0200: "WM_MOUSEMOVE", 0x0201: "WM_LBUTTONDOWN", 0x0202: "WM_LBUTTONUP", 0x0204: "WM_RBUTTONDOWN",
               0x0205: "WM_RBUTTONUP", 0x0207: "WM_MBUTTONDOWN", 0x0208: "WM_MBUTTONUP", 0x020A: "WM_MOUSEWHEEL",
               0x020B: "WM_XBUTTONDOWN", 0x020C: "WM_XBUTTONUP", 0x020E: "WM_MOUSEHWHEEL"}

triggered_keys = []
process_keystroke = None
physically_pressed_keys = set()
hook_manager = None
exit_key = None
exit_event = threading.Event()


def create_hook(process_keystroke_func, key_exit):
    """
    Creates a keyboard hook.
    """
    global process_keystroke, hook_manager, exit_key, exit_event
    exit_key = key_exit
    exit_event.clear()
    process_keystroke = process_keystroke_func
    hook_manager = pyHook.HookManager()
    hook_manager.KeyAll = handle_keyboard_all
    hook_manager.HookKeyboard()
    # Create Hook for mouse manually, because the pyHook-Version does not support XBUTTONS
    pyHook.cpyHook.cSetHook(pyHook.HookConstants.WH_MOUSE_LL, mouse_handler)


def delete_hooks():
    pyHook.cpyHook.cUnhook(pyHook.HookConstants.WH_MOUSE_LL)
    hook_manager.UnhookKeyboard()


def pump_messages(update, pump_messages_delay):
    """
    Pumps messages until Hook.exit_event is set.
    """

    while not exit_event.is_set():
        update()
        pythoncom.PumpWaitingMessages()
        time.sleep(pump_messages_delay)
    delete_hooks()


def end_pumping():
    global exit_event
    exit_event.set()


# noinspection PyUnusedLocal
def mouse_handler(msg, _x, _y, data, _flags, _time, _hwnd, _window_name):
    try:
        name = MOUSE_CODES[msg]
    except:
        raise Exception("Unknown Mouse Event: Msg={}".format(hex(msg)))

    # bypass for non-button mouse events
    if name in ("WM_MOUSEMOVE", "WM_MOUSEWHEEL", "WM_MOUSEHWHEEL"):
        return True

    assert name[-2:] == "UP" or name[-4:] == "DOWN"
    key_down = (name[-4:] == "DOWN")
    relevant_data = data >> 16

    key_name = name[3]
    if key_name == "L":  # Left mouse button
        mouse_event_id = 0x01
    elif key_name == "R":  # Right mouse button
        mouse_event_id = 0x02
    elif key_name == "M":  # Middle mouse button
        mouse_event_id = 0x04
    elif key_name == "X":  # one of the two XBUTTONS (thumb buttons)
        if relevant_data & 0x0001 > 0:  # XBUTTON 1
            mouse_event_id = 0x05
        elif relevant_data & 0x0002 > 0:  # XBUTTON 2
            mouse_event_id = 0x06
        else:
            raise Exception("Unknown XBUTTON event: Name={0}, Data={1}".format(name, relevant_data))
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
    key_down = (event.IsTransition() == 0)

    if int(exit_key) == event.KeyID and key_down:
        end_pumping()

    # Workaround: Sending ALT-TAB does not work in Win 8 because of new security mechanisms. Generating key presses
    # always leads to keyboard events where the injected bit is set and Windows 8 ignores Alt-Tab if this bit is set.
    # This workaround simply lets the physically (and not injected) pressed Tab key through if the Alt key is already
    # pressed. So it's possible to use Alt-Tab with this workaround, but it's not possible to get the functionality
    # of Alt-Tab on other keys.
    if event.KeyID == 0x09 and 164 in physically_pressed_keys:
        return True

    # If the german keyboard layout is selected, pressing the right Alt key also sends the left control key. This key
    # gets filtered here.
    if event.KeyID == 162 and event.ScanCode == 541:
        return False

    # Numpad return and normal return share the same virtual key code. They can be differentiated by the extended flag.
    # If the flag is set, the numpad key has been pressed. The numpad return key gets the virtual key code 0x88,
    # which is an unused windows virtual key. This allows to distinguish betwenn numpad / normal return key.
    if event.KeyID == 0x0D and event.IsExtended():
        event.KeyID = 0x88

    # 0xE7 is the virtual key code for VK_PACKET. VK_PACKET keyboard events represent unicode characters as key
    # events. Since this programm generates these messages and is not supposed to react on them, VK_PACKET events
    # should pass.
    if event.KeyID == 0xE7:
        return True

    return filter_dublicates(event.KeyID, key_down)


def filter_dublicates(key_id, key_down):
    # Check if event was triggered by the program
    if (key_id, key_down) in triggered_keys:
        triggered_keys.remove((key_id, key_down))
        return True

    # While holding a key, the keyboard sends key pressed events repeatingly. Only the first key pressed and key
    # released events should be considered.
    if key_down and key_id not in physically_pressed_keys:  # First key pressed event
        physically_pressed_keys.add(key_id)
        process_keystroke(key_id, key_down)
    elif not key_down and key_id in physically_pressed_keys:  # First key released event
        physically_pressed_keys.remove(key_id)
        process_keystroke(key_id, key_down)

    return False
