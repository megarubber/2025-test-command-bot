import typing
import commands2
import phoenix5
import wpilib.drive
import constants
import commands2.sysid
from wpimath.units import volts

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

        self.left_encoder = wpilib.Encoder(5, 6)
        self.right_encoder = wpilib.Encoder(7, 8, True)

        self.left_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.right_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

        self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)

        def drive(voltage: volts) -> None:
            self.left.setVoltage(voltage)
            self.right.setVoltage(voltage)

        self.sys_id_routine = commands2.sysid.SysIdRoutine(
            commands2.sysid.SysIdRoutine.Config(),
            commands2.sysid.SysIdRoutine.Mechanism(drive, self.log, self),
        )
    
    def arcadeDrive(
        self, forward: typing.Callable[[], float], rotation: typing.Callable[[], float]
    ) -> None:
        self.drivetrain.arcadeDrive(forward, rotation)

    def getLeftEncoder(self): 
        return self.left_encoder.get()

    def getRightEnconder(self):
        return self.right_encoder.get()

    def sysIdQuasistatic(self, direction: commands2.sysid.SysIdRoutine.Direction) -> commands2.Command:
        return self.sys_id_routine.quasistatic(direction)

    def sysIdDynamic(self, direction: commands2.sysid.SysIdRoutine.Direction) -> commands2.Command:
        return self.sys_id_routine.dynamic(direction)

    # Tell SysId how to record a frame of data for each motor on the mechanism being
    # characterized.
    def log(self, sys_id_routine: wpilib.sysid.SysIdRoutineLog) -> None:
        # Record a frame for the left motors.  Since these share an encoder, we consider
        # the entire group to be one motor.
        sys_id_routine.motor("drive-left").voltage(
            self.left.get() * wpilib.RobotController.getBatteryVoltage()
        ).position(self.left_encoder.getDistance()).velocity(
            self.left_encoder.getRate()
        )
        # Record a frame for the right motors.  Since these share an encoder, we consider
        # the entire group to be one motor.
        sys_id_routine.motor("drive-right").voltage(
            self.right.get() * wpilib.RobotController.getBatteryVoltage()
        ).position(self.right_encoder.getDistance()).velocity(
            self.right_encoder.getRate()
        )