import time
import board
import usb_hid
from adafruit_hid.gamepad import Gamepad
gp = Gamepad(usb_hid.devices)

from analogio import AnalogIn
wheel = AnalogIn(board.GP28) #where wheel [pt is attached

import neopixel
pixel_pin = board.GP18
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=10, auto_write=False)

import digitalio



button_pins = (board.GP17, board.GP16,board.GP14, board.GP12, board.GP15, board.GP8, board.GP7, board.GP2)
gamepad_buttons = (10, 9, 8, 7, 6, 4, 3, 2) 
#I don't know what buttons this maps to on a gamepad, but I use a tool called x350ce 
#that lets you map any gamepad to a virtual xbox360 controller.
buttons = [digitalio.DigitalInOut(pin) for pin in button_pins]


for button in buttons:
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
def constrain(x, m, M):
    if x<=m:
        return m
    elif x>=M:
        return M
    else:
        return x

def xM(pin, iM, iMax, oM, oMax):
    x= (pin.value * 255) // 65536 #the analong input on pico circuit python is 16 bit, which is very very precise. So we first convert it to 8 bit.
    return constrain((x - iM) * (oMax - oM) // (iMax - iM) + oM, oM, oMax) 
    # now this functions takes x as input, then maps that x in a specific range to an output range.
    # we didn;t need to first convert it to 8 bit but it helps in calibrating
    #return x ##this comment is to just debug
while True:
    
    wheelVal=xM(wheel, 3, 250, -127, 127)
    #first go to the function xM() and comment the return constrain.... and un-comment return x. then put your wheel to the right most or as right as you want
    #it to go and replace that value with 3. same with left most. 
    
    # this is completely your preference of how much understeer or oversteer you want. 
    gp.move_joysticks(x=wheelVal, y=0)
    # we move only x joystic.
    
    for i, button in enumerate(buttons):
        
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
            if i==1:
                for n in range(4, 6):
                    pixels[n] = (0,0,0)
                    pixels.show()
            elif i==0:
                for i in range(0, 2):
                    pixels[i] = (0,0,0)
                    pixels.show()
            elif i==3 :
                pixels[3] = (0,0,0)
                pixels[2] = (0,0,0)
                pixels.show()
            elif i==7 :
                pixels[2] = (0,0,0)
                pixels[3] = (0,0,0)
                pixels.show()
        else:
            if i==1:
                for n in range(4, 6):
                    pixels[n] = (0,255,0)
                    pixels.show()
            elif i==0:
                for i in range(0, 2):
                    pixels[i] = (255,0,0)
                    pixels.show()
            elif i==3 :
                pixels[3] = (0,0,255)
                pixels[2] = (0,0,0)
                pixels.show()
            elif i==7 :
                pixels[2] = (0,0,255)
                pixels[3] = (0,0,0)
                pixels.show()
            else:
                pass
            gp.press_buttons(gamepad_button_num)
