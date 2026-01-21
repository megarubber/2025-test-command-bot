from commands2 import Subsystem
from phoenix5 import WPI_VictorSPX
import constants

class Climber(Subsystem):
    def __init__(self) -> None:
        self.motor = WPI_VictorSPX(constants.kClimberMotor)
    
    def front(self) -> None:
        self.motor.set(1)
    
    def back(self) -> None:
        self.motor.set(-1)