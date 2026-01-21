import constants
import commands2.cmd

from commands2.button import CommandXboxController
from commands2.sysid import SysIdRoutine
from pathplannerlib.auto import AutoBuilder

from subsystems.drivetrain import Drivetrain
from subsystems.camera import Camera

from wpilib import SmartDashboard

class RobotContainer:
    def __init__(self) -> None:
        self.drivetrain = Drivetrain()
        self.camera = Camera()

        self.driver_controller = CommandXboxController(
            constants.kDriverControllerPort
        )

        self.configureButtonBindings()

        SmartDashboard.putNumber("Left", self.drivetrain.getLeftEncoder())
        SmartDashboard.putNumber("Right", self.drivetrain.getRightEncoder())
        
        #self.autoChooser = AutoBuilder.buildAutoChooser()
        
        self.drivetrain.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.atualizar(),
                self.drivetrain
            )
        )

    def atualizar(self):
        SmartDashboard.putNumber("Left", self.drivetrain.getLeftEncoder())
        SmartDashboard.putNumber("Right", self.drivetrain.getRightEncoder())

    def configureButtonBindings(self) -> None:
        '''
        self.driver_controller.a().onTrue(
            commands2.cmd.runOnce(
                lambda: self.camera.write(50)
            )
        )
    
        self.driver_controller.b().onTrue(
            commands2.cmd.runOnce(
                lambda: self.camera.write(49)
            )
        )
        '''
        self.driver_controller.a().whileTrue(
            self.drivetrain.sysIdQuasistatic(SysIdRoutine.Direction.kForward)
        )
        self.driver_controller.b().whileTrue(
            self.drivetrain.sysIdQuasistatic(SysIdRoutine.Direction.kReverse)
        )
        self.driver_controller.x().whileTrue(
            self.drivetrain.sysIdDynamic(SysIdRoutine.Direction.kForward)
        )
        self.driver_controller.y().whileTrue(
            self.drivetrain.sysIdDynamic(SysIdRoutine.Direction.kReverse)
        )
        self.driver_controller.leftBumper().whileTrue(
            commands2.cmd.run(lambda: self.drivetrain.resetPose())
        )

    def getAutonomousCommand(self) -> None:
        return commands2.cmd.none()