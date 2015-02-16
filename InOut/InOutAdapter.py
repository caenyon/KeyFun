from InOut import Send, Hook

__author__ = 'Felix'


class InOutAdapter(object):
    def __init__(self):
        pass

    def create_input_hook(self, process_keystroke_func, exit_key):
        Hook.create_hook(process_keystroke_func, exit_key)

    def pump_messages(self, update_func, delay):
        Hook.pump_messages(update_func, delay)

    def send_key(self, key_id, down):
        if key_id in (1, 2, 4, 5, 6):
            self.send_mouse_key(key_id, down)
        else:
            self.send_keyboard_key(key_id, down)

    def send_mouse_key(self, key_id, down):
        Hook.triggered_keys.append((key_id, down))
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

        Hook.triggered_keys.append((key_id, down))
        Send.send_keyboard_input(key_id, down, unicode_key=False, extended_flag=extended_flag)

    def send_unicode_key(self, unicode_id, down):
        Send.send_keyboard_input(unicode_id, down, unicode_key=True)

