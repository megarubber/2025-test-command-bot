import constants

from commands2.sysid import SysIdRoutine
from typing import Callable
from commands2 import Subsystem, Command
#from phoenix5 import WPI_VictorSPX, NeutralMode
from rev import SparkMax, SparkMaxConfig, ResetMode, PersistMode
from wpilib.drive import DifferentialDrive
from wpimath.geometry import Rotation2d, Pose2d
from wpimath.units import volts
from wpilib import RobotController, Encoder, SmartDashboard
from wpilib.sysid import SysIdRoutineLog
from pathplannerlib.auto import AutoBuilder
from pathplannerlib.controller import PPLTVController
from pathplannerlib.config import RobotConfig
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import DifferentialDriveOdometry, ChassisSpeeds
from navx import AHRS

class Drivetrain(Subsystem):
    def __init__(self) -> None:
        super().__init__()
        #self.left1 = WPI_VictorSPX(constants.kLeftMotor1Port)
        #self.left2 = WPI_VictorSPX(constants.kLeftMotor2Port)
        #self.right1 = WPI_VictorSPX(constants.kRightMotor1Port)
        #self.right2 = WPI_VictorSPX(constants.kRightMotor2Port)

        self.left1 = SparkMax(constants.kLeftMotor1Port, constants.kBrushless)
        self.left2 = SparkMax(constants.kLeftMotor2Port, constants.kBrushless)
        self.right1 = SparkMax(constants.kRightMotor1Port, constants.kBrushless)
        self.right2 = SparkMax(constants.kRightMotor2Port, constants.kBrushless)

        self.right2.follow(self.right1)
        self.right1.setInverted(True)
        self.right2.setInverted(True)

        self.left2.follow(self.left1)

        self.config = SparkMaxConfig()

        config.smartCurrentLimit(constants.kSmartCurrentLimit)
        config.idleMode(constants.kMotorIdle)
        config.encoder.positionConversionFactor(constants.kRotationToMeters)
        config.encoder.velocityConversionFactor(constants.kRotationsPerMinuteToMetersPerSeconds)

        self.left1.config(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.follow(self.left1)

        self.left2.config(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.follow(self.right1)
        self.right2.config(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        config.disableFollowerMode()
        self.right1.config(
            config, ResetMode.kResetSafeParameters, PersistMode.kPersistParameters
        )

        #self.left1.setNeutralMode(NeutralMode.Brake)
        #self.left2.setNeutralMode(NeutralMode.Brake)

        #self.right1.setNeutralMode(NeutralMode.Brake)
        #self.right2.setNeutralMode(NeutralMode.Brake)

        #self.left_encoder = Encoder(*constants.kLeftEncoderPorts)
        #self.right_encoder = Encoder(*constants.kRightEncoderPorts)

        #self.left_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        #self.right_encoder.setDistancePerPulse(constants.kEncoderDistancePerPulse)
        
        self.left_encoder = self.left1.getEncoder()
        self.right_encoder = self.right1.getEncoder()
        
        self.navx = AHRS.create_spi()
        self.navx.reset()

        self.drivetrain = DifferentialDrive(self.left1, self.right1)
                
        self.pose = Pose2d(*constants.kInitialPose)
        
        self.odometry = DifferentialDriveOdometry(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            0, 0,
            self.pose
        )

        self.relativeSpeed = ChassisSpeeds()

        config = RobotConfig.fromGUISettings()
        
        '''
        AutoBuilder.configure(
            self.pose, # Robot pose supplier
            self.resetPose, # Method to reset odometry (will be called if your auto has a starting pose)
            self.relativeSpeed, # ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            lambda speeds, feedforwards: self.driveRobotRelative(speeds), # Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also outputs individual module feedforwards
            PPLTVController(0.02), # PPLTVController is the built in path following controller for differential drive trains
            config, # The robot configuration
            self.shouldFlipPath, # Supplier to control path flipping based on alliance color
            self # Reference to this subsystem to set requirements
        )
        '''

        def drive(voltage: volts) -> None:
            self.left1.setVoltage(voltage)
            self.right1.setVoltage(voltage)

        self.sys_id_routine = SysIdRoutine(
            SysIdRoutine.Config(),
            SysIdRoutine.Mechanism(drive, self.log, self),
        )
    
    def arcadeDrive(
        self, forward: Callable[[], float], rotation: Callable[[], float]
    ) -> None:
        self.drivetrain.arcadeDrive(forward, rotation)
    
    def resetPose(self) -> None:
        self.pose = Pose2d(*constants.kInitialPose)
        self.odometry.resetPosition(
            Rotation2d.fromDegrees(self.navx.getAngle()),
            0, 0,
            self.pose
        )
        self.left_encoder.reset()
        self.right_encoder.reset()

    def getLeftEncoder(self) -> int: 
        return self.left_encoder.get()

    def getRightEncoder(self) -> int:
        return self.right_encoder.get()

    def sysIdQuasistatic(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sys_id_routine.quasistatic(direction)

    def sysIdDynamic(self, direction: SysIdRoutine.Direction) -> Command:
        return self.sys_id_routine.dynamic(direction)

    def log(self, sys_id_routine: SysIdRoutineLog) -> None:
        sys_id_routine.motor("drive-left").voltage(
            self.left1.get() * RobotController.getBatteryVoltage()
        ).position(self.left_encoder.getDistance()).velocity(
            self.left_encoder.getRate()
        )
        
        sys_id_routine.motor("drive-right").voltage(
            self.right1.get() * RobotController.getBatteryVoltage()
        ).position(self.right_encoder.getDistance()).velocity(
            self.right_encoder.getRate()
        )