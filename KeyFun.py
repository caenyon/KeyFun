# -*- coding: utf-8 -*-
"""
KeyFun is a program that allows key bindings, rearrangements and more.
"""
import logging
import threading

__author__ = 'Felix'

from Hook import Hook
from GUI import KeyboardGUI

logging.getLogger().setLevel(logging.DEBUG)

exit_flag = threading.Event()

hook_thread = threading.Thread(target=Hook.run, name='HookThread')
hook_thread.start()

keyboard_gui = KeyboardGUI(Hook.highlight_keys, Hook.reset_highlight_keys, Hook.simulated_keys, Hook.pause_flag)
keyboard_gui.run()

gui_thread = threading.Thread(target=keyboard_gui.run, name='GuiThread')
gui_thread.start()

while not keyboard_gui.exit_flag.isSet():
    pass

Hook.exit_flag.set()

gui_thread.join()
hook_thread.join()
