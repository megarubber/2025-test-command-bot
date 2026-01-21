from wpilib import SerialPort

from math import pi

kDriverControllerPort = 0
kLeftMotor1Port = 1
kLeftMotor2Port = 2
kRightMotor1Port = 3
kRightMotor2Port = 4
kBaudRate = 9600
kUSBPort = SerialPort.Port.kUSB1
kEncoderPPR = 2048.0
kWheelDiameter = 0.152
kGearRatio = 10.7
kLeftEncoderPorts = (0, 1)
kRightEncoderPorts = (3, 4, True)
kEncoderDistancePerPulse = (kWheelDiameter * pi) / (kEncoderPPR * kGearRatio)
kClimberMotor = 12
kInitialPose = (0, 0, 0) # x, y and theta