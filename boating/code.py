# import board support libraries, including HID.
import board
import analogio
import usb_hid

from time import sleep

from adafruit_hid.keycode import Keycode
from hid_gamepad import Gamepad

# local functions
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def read_analog():
    x = ax.value - x_offset
    y = ay.value - y_offset
    return x, y

throttle_value = 0
steering_value = 0


# game pad key configuration
keyboard_buttons = {    Keycode.W : 1, Keycode.C : 2, Keycode.S : 3, 
                        Keycode.A : 4, Keycode.Y : 5, Keycode.D : 6
                    }

# game pad joystick configuration (x/y values)
gp = Gamepad(usb_hid.devices)


def press_button(key):
    gp.press_buttons(keyboard_buttons[key]) 
    sleep(0.05)
    gp.release_buttons(keyboard_buttons[key])
    sleep(0.05)
    
# setup analogue inputs
ax = analogio.AnalogIn(board.GP26)
ay = analogio.AnalogIn(board.GP27)

global x_offset
global y_offest

x_offset = y_offset = 0

# calibrate to zero on startup
x_offset, y_offset = read_analog()

# initialize filters
y_filter = y_offset
x_filter = x_offset

# find max range after calibration
x_max_offset = abs(32768 - x_offset)
x_max_range = 32768 + x_max_offset + 200
y_max_offset = abs(32768 - y_offset)
y_max_range = 32768 + y_max_offset + 200

print('Looping.')
while True:
    
    # read current analog value
    x_value, y_value = read_analog()
    
    # filter signal
    y_value = y_filter * 0.8 + y_value * 0.2
    y_filter = y_value
    
    x_value = x_filter * 0.9 + x_value * 0.1
    x_filter = x_value
    
    # update values directly in joystick
    x = range_map(int(x_value), -x_max_range, x_max_range, -127, 127)
    y = range_map(int(y_value), -y_max_range, y_max_range, -127, 127)
        
    gp.move_joysticks(
        x=x,
        y=y,
    )
    
    # handle throttle control with keys
    throttle_pos = int(round((10.0 / 15000.0) * y_value))

    if throttle_pos == 0 and throttle_value != 0:
        press_button(Keycode.C)
        throttle_value = 0
    else:
        if throttle_pos > throttle_value:
            press_button(Keycode.S)
            throttle_value += 1
            
        if throttle_pos < throttle_value:
            press_button(Keycode.W)
            throttle_value -= 1

    # handle steering with keys
    steering_pos = int(round((12.0 / 26000.0) * x_value))

    if steering_pos == 0 and steering_value != 0:
        press_button(Keycode.Y)
        steering_value = 0
    else:
        if steering_pos > steering_value:
            press_button(Keycode.A)
            steering_value += 1
            
        if steering_pos < steering_value:
            press_button(Keycode.D)
            steering_value -= 1
    
    #print("{:.1f} {:.1f}".format(throttle_pos, y_value))
    #print("{:.1f} {:.1f}".format(x, y))
 
