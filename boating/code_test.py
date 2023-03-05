#import board support libraries, including HID.
import board
import analogio
import usb_hid


from time import sleep

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from hid_gamepad import Gamepad

from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

mediacontrol = ConsumerControl(usb_hid.devices)

keyboard = Keyboard(usb_hid.devices)
gp = Gamepad(usb_hid.devices)

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# setup analogue inputs
ax = analogio.AnalogIn(board.GP26)
ay = analogio.AnalogIn(board.GP27)

global x_offset
global y_offest

x_offset = y_offset = 0

def read_analog():
    x = ax.value - x_offset
    y = ay.value - y_offset
    return x, y

# calibrate to zero on startup
x_offset, y_offset = read_analog()

# esail cannot handle continuous values, but only key presses
steer_pos_presses = 0
throttle_pos_presses = 0

def press_button(key):
    keyboard.press(key) 
    sleep(0.1)
    keyboard.release(key)
    sleep(0.1)

while True:
    
    # read current analog value
    x_value, y_value = read_analog()
     
    # convert to total button presses for this position
    steer_pos = int(round((14.0/30000) * x_value))
    throttle_pos = int(round((7.0/20000) * y_value))

#     if steer_pos > steer_pos_presses:
#         press_button(Keycode.A)
#         steer_pos_presses += 1
#         
#     if steer_pos < steer_pos_presses:
#         press_button(Keycode.D)
#         steer_pos_presses -= 1
# 
#     if throttle_pos > throttle_pos_presses:
#         press_button(Keycode.S)
#         throttle_pos_presses += 1
#         
#     if throttle_pos < throttle_pos_presses:
#         press_button(Keycode.W)
#         throttle_pos_presses -= 1
        
    #print("{:.1f} {:.1f}".format((14.0/30000) * x_value, (7.0/20000) * y_value))

    # update values directly in joystick
    x_value = range_map(ax.value, 0, 65535, -127, 127)
    y_value = range_map(ay.value, 0, 65535, -127, 127)
        
    gp.move_joysticks(
        x=x_value,
        y=y_value,
    )
    
    print("{:.1f} {:.1f}".format(x_value, y_value))
    
    sleep(0.1)
    
    
    
#import board support libraries, including HID.
import board
import analogio
import usb_hid


from time import sleep

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from hid_gamepad import Gamepad

gp = Gamepad(usb_hid.devices)

def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# setup analogue inputs
ax = analogio.AnalogIn(board.GP26)
ay = analogio.AnalogIn(board.GP27)

global x_offset
global y_offest

x_offset = y_offset = 0

def read_analog():
    x = ax.value - x_offset
    y = ay.value - y_offset
    return x, y

# calibrate to zero on startup
x_offset, y_offset = read_analog()

print(x_offset, y_offset)

# find max range
x_max_offset = abs(32768 - x_offset)
x_max_range = 32768 + x_max_offset + 200
y_max_offset = abs(32768 - y_offset)
y_max_range = 32768 + y_max_offset + 200

while True:
    
    # read current analog value
    x_value, y_value = read_analog()
    
    # update values directly in joystick
    x = range_map(x_value, -x_max_range, x_max_range, -127, 127)
    y = range_map(y_value, -y_max_range, y_max_range, -127, 127)
        
    gp.move_joysticks(
        x=x,
        y=y,
    )
    print("{:.1f} {:.1f} {:.1f} {:.1f}".format(x, x_value, y, y_value))
    
    sleep(0.1)
    

    
