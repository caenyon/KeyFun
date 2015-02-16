import time

from InOut import Send

time.sleep(3)
key_id = 6
Send.send_mouse_input(key_id, True)
time.sleep(1)
Send.send_mouse_input(key_id, False)
#
# print("start")
# Send.send_keyboard_input(int(VirtualKey("LSHIFT")), True)
# time.sleep(5)
# print("2")
# Send.send_keyboard_input(int(VirtualKey("LSHIFT")), False)
# time.sleep(5)
# print("3")
#
# print("end")
#
