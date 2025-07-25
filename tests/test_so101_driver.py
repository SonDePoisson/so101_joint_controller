import os
import pygame
from so101_driver.so101_driver import SO101Driver
import time
import sys

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
    device = os.getenv("SO101_PORT", "/dev/ttyUSB0")
    driver = SO101Driver(device)
    print("Detected servo IDs:", driver.servo_ids)

    try:
        while True:
            positions = []
            for servo_id in driver.servo_ids:
                pos = driver.read_servo_position(servo_id)
                positions.append(f"{pos:5}" if pos is not None else " None")
            line = " | ".join([f"ID{idx+1}: {p}" for idx, p in enumerate(positions)])
            print(f"\r{line}", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExit")
    finally:
        driver.stop_robot()
        pygame.quit()
