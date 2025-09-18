import commands2
import commands2.button
import commands2.cmd
import constants

from commands2.sysid import SysIdRoutine

from subsystems.drivetrain import Drivetrain
from subsystems.camera import Camera

class RobotContainer:
    def __init__(self) -> None:
        self.drivetrain = Drivetrain()
        self.camera = Camera()

        self.driver_controller = commands2.button.CommandXboxController(
            constants.kDriverControllerPort
        )

        self.configureButtonBindings()
        '''
        self.robot_drive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robot_drive.arcadeDrive(
                    -self.driver_controller.getLeftY(),
                    self.driver_controller.getRightX()
                ),
                self.robot_drive
            )
        )
        '''
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

    def getAutonomousCommand(self) -> None:
        return commands2.cmd.none()