'''
bt1 - 25(GP19)
bt2 - 26(GP20)
btj - 19(GP22)
jox - 31(GP26/ADC0)
joy - 32(GP27/ADC1)
'''

import board
import time
import usb_hid

from digitalio import DigitalInOut, Direction, Pull
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

bt1 = DigitalInOut(board.GP19)
bt1.direction = Direction.INPUT
bt1.pull = Pull.UP

bt2 = DigitalInOut(board.GP20)
bt2.direction = Direction.INPUT
bt2.pull = Pull.UP

btj = DigitalInOut(board.GP22)
btj.direction = Direction.INPUT
btj.pull = Pull.UP

keyboard=Keyboard(usb_hid.devices)
bt1Released = True
bt2Released = True
btjReleased = True
AltTabToggle = False
AltTabCounter = 0

def windowsTaskbarSwitch(number):
        if number > 9:
            return
        keyCode = number + 29
        keyboard.press(Keycode.GUI)
        keyboard.press(keyCode)
        keyboard.release(keyCode)
        keyboard.press(keyCode)
        keyboard.release(keyCode)
        time.sleep(0.2)
        keyboard.release(Keycode.GUI)

while True:
    if not bt1.value and bt1Released:
        #Windows
        windowsTaskbarSwitch(1)
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.M)
        bt1Released = False
    if bt1.value and not bt1Released:
        bt1Released = True

    if not bt2.value and bt2Released:
        #Windows
        windowsTaskbarSwitch(1)
        keyboard.send(Keycode.CONTROL, Keycode.SHIFT, Keycode.O)
        bt2Released = False
    if bt2.value and not bt2Released:
        bt2Released = True

    if not btj.value and btjReleased:
        AltTabCounter = 0
        if not AltTabToggle:
            keyboard.press(Keycode.ALT, Keycode.TAB)
            keyboard.release(Keycode.TAB)
            time.sleep(0.2)
            keyboard.press(Keycode.LEFT_ARROW)
            keyboard.release(Keycode.LEFT_ARROW)
        else:
            keyboard.release(Keycode.TAB)
            keyboard.release(Keycode.ALT)
        btjReleased = False
    elif btj.value and not btjReleased:
        btjReleased = True
        AltTabToggle = not AltTabToggle
    
    if AltTabCounter > 20000:
        AltTabCounter = 0
        keyboard.release(Keycode.TAB)
        keyboard.release(Keycode.ALT)
        AltTabToggle = False
    if AltTabToggle:
        AltTabCounter += 1