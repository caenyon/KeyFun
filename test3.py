import time

import Send


print("start")
Send.press_key(0x5B)
Send.press_key(0x52)

# time.sleep(1)
Send.release_key(0x52)
# time.sleep(1)
Send.release_key(0x5B)

print("end")

