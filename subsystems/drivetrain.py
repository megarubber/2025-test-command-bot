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

        self.right1.follow(self.right2)
        self.right1.setInverted(True)

        self.left1.follow(self.left2)

        self.left_encoder = wpilib.Encoder(*constants.kLeftEncoderPorts)
        self.right_encoder = wpilib.Encoder(*constants.kRightEncoderPorts)

        self.left_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        self.right_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)

        #self.drivetrain = wpilib.drive.DifferentialDrive(self.left, self.right)

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

    def getLeftEncoder(self) -> int: 
        return self.left_encoder.get()

    def getRightEnconder(self) -> int:
        return self.right_encoder.get()

    def sysIdQuasistatic(self, direction: commands2.sysid.SysIdRoutine.Direction) -> commands2.Command:
        return self.sys_id_routine.quasistatic(direction)

    def sysIdDynamic(self, direction: commands2.sysid.SysIdRoutine.Direction) -> commands2.Command:
        return self.sys_id_routine.dynamic(direction)

    def log(self, sys_id_routine: wpilib.sysid.SysIdRoutineLog) -> None:
        sys_id_routine.motor("drive-left").voltage(
            self.left1.get() * wpilib.RobotController.getBatteryVoltage()
        ).position(self.left_encoder.getDistance()).velocity(
            self.left_encoder.getRate()
        )
        
        sys_id_routine.motor("drive-right").voltage(
            self.right1.get() * wpilib.RobotController.getBatteryVoltage()
        ).position(self.right_encoder.getDistance()).velocity(
            self.right_encoder.getRate()
        )