import os
from so101_driver.so101_driver import SO101Driver

if __name__ == "__main__":
    device = os.getenv("SO101_PORT", "/dev/ttyUSB0")
    driver = SO101Driver(device)
    print("Detected servo IDs:", driver.servo_ids)
    
    driver.read_servo_state(6)
    
    driver.move_servo(6, 2664)