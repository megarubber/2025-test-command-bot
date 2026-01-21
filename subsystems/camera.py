import commands2
import typing
import wpilib
import constants

class Camera(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.arduino = wpilib.SerialPort(
            constants.kBaudRate, constants.kUSBPort
        )
    
    def write(self, value: int) -> None:
        self.arduino.write(value.to_bytes(1, 'big'))