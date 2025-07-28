# so101_joint_controller

This project is a simple exploration of the SO101 robot and serves as a starting point for developing a basic driver for the ST3215 servos and the [so101_ros project](https://github.com/SonDePoisson/so101_ros).

It is intended for learning, experimentation, and initial development of control software for the SO101 robotic arm, including joint calibration and basic gamepad-based control.

## Usage

### Calibration

To calibrate the robot joints, use the calibration script :

```Bash
python -m so101_driver.calibration
```

This script allows you to manually move each joint and record its minimum, maximum, and zero positions.  
The calibration data is saved in the `joint_limits.yaml` file, which is required by other scritps.

### Testing and Control

You can control the robot using a gamepad with the test script:

```bash
python -m tests.test_so101_driver
```

- Use the LB/RB Buttons to select different joints.
- Use the triggers to move the selected joint within its calibrated limits.
- Press the START button to reset all joints to their zero position.
- Hold the B button to release the robot (disable torque for manual movement).
- Hold the A button to move joints more slowly.

Make sure your gamepad is connected and recognized by the system before running the script.

## Requirements

- Python 3.10
- `pygame`
- `pyyaml`
- The SO101 robot and ST3215 servo driver

## Note

This project is experimental and intended for learning and prototyping.  
Feel free to adapt and extend it for your own projects and needs.
