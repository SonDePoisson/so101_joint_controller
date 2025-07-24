import os
import pygame
from so101_driver.so101_driver import SO101Driver
import time

# --- Gamepad constants for Stadia controller ---
AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 3
AXIS_RIGHT_TRIGGER = 4  # RT
AXIS_LEFT_TRIGGER  = 5  # LT

BUTTON_A      = 0
BUTTON_B      = 1
BUTTON_X      = 2
BUTTON_Y      = 3
BUTTON_LB     = 4
BUTTON_RB     = 5
BUTTON_SELECT = 6
BUTTON_START  = 7
BUTTON_STADIA = 8
BUTTON_LS     = 9  # Left stick press
BUTTON_RS     = 10 # Right stick press
# ------------------------------------------------

if __name__ == "__main__":
    # Init robot
    device = os.getenv("SO101_PORT", "/dev/ttyUSB0")
    driver = SO101Driver(device)
    print("Detected servo IDs:", driver.servo_ids)

    # Init gamepad
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        print("No joystick detected.")
        exit(1)
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Joystick detected: {joystick.get_name()}")

    servo_ids = driver.servo_ids
    current_index = 0
    current_servo = servo_ids[current_index]
    position = driver.read_servo_position(current_servo)  # Position initiale du servo
    step = 50        # Pas d'incrément/décrément

    prev_lb = 0
    prev_rb = 0

    try:
        while True:
            pygame.event.pump()

            lb = joystick.get_button(BUTTON_LB)
            rb = joystick.get_button(BUTTON_RB)

            if lb and not prev_lb:
                current_index = (current_index - 1) % len(servo_ids)
                current_servo = servo_ids[current_index]
                print(f"\nSwitched to servo {current_servo}")
            if rb and not prev_rb:
                current_index = (current_index + 1) % len(servo_ids)
                current_servo = servo_ids[current_index]
                print(f"\nSwitched to servo {current_servo}")

            prev_lb = lb
            prev_rb = rb

            lt = joystick.get_axis(AXIS_LEFT_TRIGGER)
            rt = joystick.get_axis(AXIS_RIGHT_TRIGGER)

            if rt > 0.5:
                position += step
            if lt > 0.5:
                position -= step

            position = max(0, min(4095, position))

            driver.move_servo(current_servo, position)
            real_position = driver.read_servo_position(current_servo)

            print(f"Servo {current_servo} | Target: {position} | Real: {real_position}", end='\r')

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExit")

    finally:
        pygame.quit()
