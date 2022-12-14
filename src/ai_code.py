import pygame
import serial


def get_write_value(buttons, x, y):
    val = (buttons & 0xFFFF) | ((x & 0xFF) << 16) | ((y & 0xFF) << 24)
    return val.to_bytes(4, 'little')

#initialize the serial connection to the teensy
print("Attempting to connect to usb device...beep...boop")
ser = serial.Serial("/dev/ttyACM0", 115200)
print("Successfully connected!")

# Initialize Pygame and the joystick
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

# Print information about the joystick
print("Attempting to find and connect to joystick...")
print("Found Joystick! Name of the joystick:", pygame.joystick.Joystick(0).get_name())
print("Number of axis:", pygame.joystick.Joystick(0).get_numaxes())
print("Ready to play!")
x = 0
y = 0
buttons = 0

# Process joystick events
while True:
    buttons = (pygame.joystick.Joystick(0).get_button(0) << 0 | # A button (Cross)
    pygame.joystick.Joystick(0).get_button(3) << 1 | # B button (Square)
    pygame.joystick.Joystick(0).get_button(4) << 2) # Z button (Left bumper)
    ser.write(get_write_value(buttons, x, y))
    x = int(pygame.joystick.Joystick(0).get_axis(0) * 128)
    y = int(pygame.joystick.Joystick(0).get_axis(1) * -127)
    ser.write(get_write_value(buttons, x, y))
    buttons = (buttons | pygame.joystick.Joystick(0).get_button(1) << 14)
    ser.write(get_write_value(buttons,x,y))
    # buttons = pygame.joystick.Joystick(0).get_button(0)
    # buttons += pygame.joystick.Joystick(0).get_button(3) * 2**1
    # buttons += pygame.joystick.Joystick(0).get_button(4) * 2**2
