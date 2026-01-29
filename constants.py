from wpilib import SerialPort
from rev import SparkLowLevel, SparkBaseConfig

from math import pi

kDriverControllerPort = 0
kLeftMotor1Port = 52
kLeftMotor2Port = 51
kRightMotor1Port = 53
kRightMotor2Port = 55
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
kBrushless = SparkLowLevel.MotorType.kBrushless
kSmartCurrentLimit = 40
kWheelCircumference = pi * kWheelDiameter
kRotationsToMeters = kWheelCircumference / kGearRatio
kRotationsPerMinuteToMetersPerSecond = kRotationsToMeters / 60
kMotorIdle = SparkBaseConfig.IdleMode.kBrake