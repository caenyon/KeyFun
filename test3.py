import time

import Send


print("start")
Send.press_key(164)
Send.press_key(0x11)

# time.sleep(1)
Send.press_key(9)
Send.release_key(9)
Send.release_key(0x11)
# time.sleep(1)
Send.release_key(164)

print("end")

