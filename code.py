import time
import board
import usb_hid
from adafruit_hid.gamepad import Gamepad
gp = Gamepad(usb_hid.devices)
from analogio import AnalogIn
wheel = AnalogIn(board.GP28)
import neopixel
pixel_pin = board.GP18
num_pixels = 6
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=10, auto_write=False)
import digitalio
green = digitalio.DigitalInOut(board.GP11)
green.direction = digitalio.Direction.OUTPUT
red = digitalio.DigitalInOut(board.GP10)
red.direction = digitalio.Direction.OUTPUT
yel = digitalio.DigitalInOut(board.GP9)
yel.direction = digitalio.Direction.OUTPUT



button_pins = (board.GP17, board.GP16,board.GP14, board.GP12, board.GP15, board.GP8, board.GP7, board.GP2)
gamepad_buttons = (10, 9, 8, 7, 6, 4, 3, 2)
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
    x= (pin.value * 255) // 65536
    return constrain((x - iM) * (oMax - oM) // (iMax - iM) + oM, oM, oMax)
    #return x
while False:
    rollVal=xM(roll, 3, 250, -127, 127)
    print(rollVal)
    time.sleep(0.1)
while True:
    
    wheelVal=xM(wheel, 3, 250, -127, 127)
    gp.move_joysticks(x=wheelVal, y=0)
    
    
    
    #print(wheelVal)
    #time.sleep(0.1)
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