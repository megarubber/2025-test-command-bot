import typing
import commands2
import phoenix5
import wpilib.drive

class Drivetrain(commands2.Subsystem):
    def __init__(self) -> None:
        super().__init__()
        self.left1 = phoenix5.WPI_VictorSPX(constants.kLeftMotor1Port)
        self.left2 = phoenix5.WPI_VictorSPX(constants.kLeftMotor2Port)
        self.right1 = phoenix5.WPI_VictorSPX(constants.kRightMotor1Port)
        self.right2 = phoenix5.WPI_VictorSPX(constants.kRightMotor2Port)

        self.left = wpilib.MotorControllerGroup(self.left1, self.left2)
        self.right = wpilib.MotorControllerGroup(self.right1, self.right2)

        self.right.setInverted(True)

        self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)