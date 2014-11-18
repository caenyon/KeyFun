import pyHook
import time
import pythoncom

__author__ = 'Felix'

triggered_keys = []
process_keystroke = None
physically_pressed_keys = set()
hook_manager = None


def create_hook(process_keystroke_func):
    """
    Creates a keyboard hook.

    :param event_all: function(func: pyHook.KeyboardEvent): bool
    """
    global process_keystroke, hook_manager
    process_keystroke = process_keystroke_func
    hook_manager = pyHook.HookManager()
    hook_manager.KeyAll = handle_keyboard_all
    hook_manager.HookKeyboard()


def pump_messages(update, pump_messages_delay):
    """
    Pumps messages until Hook.exit_flag is set.
    """

    while True:

        update()
        pythoncom.PumpWaitingMessages()
        time.sleep(pump_messages_delay)


def handle_keyboard_all(event):
    """
    Method that processes keyboard events sent by pyHook.

    :param event: the event to process
    :type event: pyHook.KeyboardEvent
    :return: boolean flag indicating if the event should be passed to the next handler
    :rtype: bool
    """
    #print event.KeyID, event.IsExtended(), event.IsTransition()


    # key_down = 1: Key pressed
    # key_down = 0: Key released
    key_down = (event.IsTransition() == 0)

    # this is the left control key that is sent with the right Alt key
    if event.KeyID == 162 and event.ScanCode == 541:
        return False

    # this is the numpad return key
    # if event.KeyID == 0x0D and event.IsExtended():
    #     event.KeyID = 1000
    # TODO: was buggy, needs to be fixed sometimes

    # check if the received key event was triggered by the program
    if (event.KeyID, key_down) in triggered_keys:
        triggered_keys.remove((event.KeyID, key_down))
        return True
    else:
        if key_down and not event.KeyID in physically_pressed_keys:
            # Key pressed event
            physically_pressed_keys.add(event.KeyID)

            process_keystroke(event.KeyID, key_down)

        elif not key_down and event.KeyID in physically_pressed_keys:
            # Key released event
            physically_pressed_keys.remove(event.KeyID)

            process_keystroke(event.KeyID, key_down)

        return False
