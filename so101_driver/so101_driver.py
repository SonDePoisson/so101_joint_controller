from st3215 import ST3215

class SO101Driver:
    """
    Driver class for controlling the SO101 robot using the st3215 library.
    """

    def __init__(self, device):
        """
        Initialize the connection to the SO101 robot serial bus.

        :param device: Serial port path (e.g., '/dev/ttyUSB0')
        """
        try:
            self.st = ST3215(device)
            self.servo_ids = self.st.ListServos()
        except Exception as e:
            print("SO101Driver init:", e)
            raise

    def move_servo(self, servo_id, position, speed=2400, acc=50, wait=False):
        """
        Move a servo to a target position.

        :param servo_id: ID of the servo to move
        :param position: Target position
        :param speed: Movement speed
        :param acc: Acceleration
        :param wait: Wait for movement to finish
        """
        return self.st.MoveTo(servo_id, position, speed, acc, wait)
    
    def read_servo_position(self, servo_id):
        """
        Read the current position of a servo.

        :param servo_id: ID of the servo to read
        :return: Position value or None if error
        """
        try:
            position = self.st.ReadPosition(servo_id)
            return position
        except Exception as e:
            print(f"Error reading position for servo {servo_id}:", e)
            return None

    def read_servo_state(self, servo_id):
        """
        Read and display the state of a servo: status, position, velocity, acceleration.

        :param servo_id: ID of the servo to read
        :return: dict with status, position, velocity, acceleration
        """
        try:
            position = self.st.ReadPosition(servo_id)
            velocity = self.st.ReadSpeed(servo_id)
            acceleration = self.st.ReadAccelaration(servo_id)
            status = self.st.ReadStatus(servo_id)
        except Exception as e:
            print(f"Error reading servo {servo_id} state:", e)
            return None

        state = {
            "id": servo_id,
            "status": status,
            "position": position,
            "velocity": velocity,
            "acceleration": acceleration
        }

        # Présentation propre dans le terminal
        print(f"\nServo {servo_id} state:")
        print(f"  Status      : {status}")
        print(f"  Position    : {position}")
        print(f"  Velocity    : {velocity}")
        print(f"  Acceleration: {acceleration}")

        return state
