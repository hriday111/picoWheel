import time
import board
import usb_hid
from adafruit_hid.gamepad import Gamepad
import digitalio
from analogio import AnalogIn
wheel = AnalogIn(board.GP28) #where wheel [pt is attached
offset= 0 #offset will be set when the wheel goes too far too left or right
debug=True
wheelMin=0
wheelMax=1024
wheelOffsetMin=0
wheelOffsetMax=1024


gp = Gamepad(usb_hid.devices)
##                accelator   brake    button1     button2     button3     button4        
button_pins = (board.GP17, board.GP16, board.GP15, board.GP14, board.GP13, board.GP12, board.GP11, board.GP4)
gamepad_buttons = (10, 9, 8, 7, 6, 4, 3, 2) 

#The code is going to be in such a way so that when button on GP17 is pressed, pico sends a button10 of a gamepad to the PC
#Button 5 and 6 are for setting offset, but also sends gamepad data to the PC.
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

def xM(pin, inMin, inMax, outMin, outMax, debug=False):
    x= (pin.value * 1025) // 65536 #the analong input on pico circuit python is 16 bit, which is very very precise. So we first convert it to 8 bit.
    if not debug:
        return constrain((x - inMin) * (outMax - outMin) // (inMax - inMin) + outMin, outMin, outMax) 
        # now this functions takes x as input, then maps that x in a specific range to an output range. And also constrains it from outMin to outMax

    return x 



while True:
    
    wheelVal=xM(wheel, wheelMin, wheelMax, -127, 127, debug)
    if debug:


        print(wheelVal)
        time.sleep(0.1)

        # DEBUG TEST 1
        #First put your wheel to left most position and give that value to wheelMin on the top of the code.
        #Then put your wheel to right position and give that value to wheelMax on the top of the code.


        
        #DEBUG TEST 2
        #First Press the accelator
        #Then put your wheel to left most position and give that value to wheelOffsetMin on the top of the code.
        #Then put your wheel to right position and give that value to wheelOffsetMax on the top of the code.
    
        ## DEBUG TEST 2 is not necessary. You can set the offsetMin and offsetMax to the same value as from DEBUG TEST 1. 
        ## But if you do notice that the wheel moves to right in the game when you press accelator brake then perform DEBUG TEST 2

    
    for i, button in enumerate(buttons):
        
        gamepad_button_num = gamepad_buttons[i]
        if button.value:
            gp.release_buttons(gamepad_button_num)
            if i==1:
                wheelMin=0 # the value you got when you performed DEBUG TEST 1
                wheelMax=1024 # the value you got when you performed DEBUG TEST 1
            elif i==0:
                wheelMin=0 # the value you got when you performed DEBUG TEST 1
                wheelMax=1024 # the value you got when you performed DEBUG TEST 1
        else:
            gp.press_buttons(gamepad_button_num)
            if i==1:
                wheelMin=wheelOffsetMin
                wheelMax=wheelOffsetMax
            elif i==0:
                wheelMin=wheelOffsetMin
                wheelMax=wheelOffsetMax
            elif i==7:
                offset-=1
            elif i==8:
                offset+=1

    gp.move_joysticks(x=constrain(wheelVal+offset,-127,127), y=0)
    # we move only x joystic.
