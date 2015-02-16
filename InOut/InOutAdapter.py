import Constants
from InOut import Send, Hook

__author__ = 'Felix'


class InOutAdapter(object):
    def __init__(self, process_keystroke_func, exit_key, print_status_func):
        self.triggered_events = []
        self.process_keystroke_func = process_keystroke_func
        self.hook = Hook.Hook(process_keystroke_func, self.triggered_events, exit_key, print_status_func)

    def run_hooks(self, update_func, delay):
        self.hook.run(update_func, delay)

    def send_key(self, key_id, down):
        print "Sending {0} {1}".format(Constants.key_id_to_name.get(key_id), "down" if down else "up")
        if key_id in (1, 2, 4, 5, 6):
            self.send_mouse_key(key_id, down)
        else:
            self.send_keyboard_key(key_id, down)

    def send_mouse_key(self, key_id, down):
        self.triggered_events.append((key_id, down))
        Send.send_mouse_input(key_id, down)

    def send_keyboard_key(self, key_id, down):
        extended_flag = None

        # If the right Alt key has been pressed/released, the left control key has to be pressed/released additionally
        # to keep the functionality of the german keyboard layout.
        if key_id == 0x5A:
            self.send_keyboard_key(0xA2, down)

        # The numpad return key has been pressed/released. Send normalal return key (0x0D) with extended flag set.
        if key_id == 0x88:
            key_id = 0x0D
            extended_flag = True

        self.triggered_events.append((key_id, down))
        Send.send_keyboard_input(key_id, down, unicode_key=False, extended_flag=extended_flag)

    # noinspection PyMethodMayBeStatic
    def send_unicode_key(self, unicode_id, down):
        print "Sending {0} {1}".format(hex(unicode_id), "down" if down else "up")
        Send.send_keyboard_input(unicode_id, down, unicode_key=True)

