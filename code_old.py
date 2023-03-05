#import board support libraries, including HID.
import board
import analogio
import usb_hid

from time import sleep

from hid_gamepad import Gamepad


#local functions
def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def read_analog():
    x = ax.value - x_offset
    y = ay.value - y_offset
    return x, y

# game pad configuration (x/y values)
gp = Gamepad(usb_hid.devices)

# setup analogue inputs
ax = analogio.AnalogIn(board.GP26)
ay = analogio.AnalogIn(board.GP27)

global x_offset
global y_offest

x_offset = y_offset = 0

# calibrate to zero on startup
x_offset, y_offset = read_analog()

# find max range after calibration
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
    
    print("{:.1f} {:.1f}".format(x, y))
    
    sleep(0.05)
    
