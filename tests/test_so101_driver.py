import os
import pygame
from so101_driver.so101_driver import SO101Driver
import time
import yaml

STEP = 200

# --- Gamepad constants for Stadia controller ---
AXIS_LEFT_STICK_X = 0
AXIS_LEFT_STICK_Y = 1
AXIS_RIGHT_STICK_X = 2
AXIS_RIGHT_STICK_Y = 3
AXIS_RIGHT_TRIGGER = 4 
AXIS_LEFT_TRIGGER  = 5 
TRIGGER_THRESHOLD = 0.2

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

    with open(os.path.join(os.path.dirname(__file__), "../joint_limits.yaml")) as f:
        joint_config = yaml.safe_load(f)
    zero_positions = joint_config["zero"]
    joint_limits = {str(k): v for k, v in joint_config["limits"].items()}

    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    current_servo_index = 0
    current_servo = driver.servo_ids[current_servo_index]
    print(f"\rSelected joint : {current_servo}", end=" ", flush=True)
    min_pos = joint_limits[str(current_servo)]["min"]
    max_pos = joint_limits[str(current_servo)]["max"]
    
    current_step = STEP

    try:
        while True:
            pygame.event.pump()
            current_pos = driver.read_servo_position(current_servo)
            time.sleep(0.05)
            
            # Slowdown Robot
            if joystick.get_button(BUTTON_A) : 
                current_step = STEP // 2
            else :
                current_step = STEP
            
            # Zero Position
            if joystick.get_button(BUTTON_START):
                for joint_id, zero_pos in zero_positions.items():
                    driver.move_servo(joint_id, zero_pos)
                time.sleep(0.5)
                
            # Free Robot
            if joystick.get_button(BUTTON_B):
                driver.free_robot()
            else :
                driver.activate_robot()
                
            # Joint Selection
            if joystick.get_button(BUTTON_LB) or joystick.get_button(BUTTON_RB):
                if joystick.get_button(BUTTON_LB):
                    current_servo_index = (current_servo_index - 1) % len(driver.servo_ids)
                if joystick.get_button(BUTTON_RB):
                    current_servo_index = (current_servo_index + 1) % len(driver.servo_ids)
                current_servo = driver.servo_ids[current_servo_index]
                print(f"\rSelected joint : {current_servo}", end=" ", flush=True)
                current_pos = driver.read_servo_position(current_servo)
                time.sleep(0.3)
                min_pos = joint_limits[str(current_servo)]["min"]
                max_pos = joint_limits[str(current_servo)]["max"]
            
            # Move Selected Joint
            if current_pos is not None :
                if joystick.get_axis(AXIS_LEFT_TRIGGER) > TRIGGER_THRESHOLD:
                    new_pos = max(current_pos - current_step, min_pos)
                    driver.move_servo(current_servo, new_pos)

                if joystick.get_axis(AXIS_RIGHT_TRIGGER) > TRIGGER_THRESHOLD:
                    new_pos = min(current_pos + current_step, max_pos)
                    driver.move_servo(current_servo, new_pos)

    except KeyboardInterrupt:
        print("\nExit")
    finally:
        driver.free_robot()
        pygame.quit()
