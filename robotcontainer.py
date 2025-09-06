import commands2
import commands2.button
import commands2.cmd

class RobotContainer:
    def __init__(self) -> None:
        self.robot_drive = Drivetrain()

        self.driver_controller = commands2.button.CommandXboxController(
            constants.OIConstants.kDriverControllerPort
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
        pass
    
    def getAutonomousCommand(self) -> None:
        return commands2.cmd.none()