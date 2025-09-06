import commands2
import commands2.button
import commands2.cmd

from subsystems.drivetrain import Drivetrain
from subsystems.camera import Camera

class RobotContainer:
    def __init__(self) -> None:
        self.robot_drive = Drivetrain()
        self.camera = Camera()

        self.driver_controller = commands2.button.CommandXboxController(
            constants.kDriverControllerPort
        )

        self.configureButtonBindings()

        self.robot_drive.setDefaultCommand(
            commands2.cmd.run(
                lambda: self.robot_drive.arcadeDrive(
                    -self.driver_controller.getLeftY(),
                    self.driver_controller.getRightX()
                )
            ),
            self.robot_drive
        )

    def configureButtonBindings(self) -> None:
        self.driver_controller.a().onTrue(
            commands2.cmd.runOnce(
                self.camera.write(50)
            )
        )
    
        self.driver_controller.b().onTrue(
            commands2.cmd.runOnce(
                self.camera.write(49)
            )
        )

    def getAutonomousCommand(self) -> None:
        return commands2.cmd.none()