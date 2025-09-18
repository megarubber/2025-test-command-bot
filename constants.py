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
kEncoderDistancePerPulse = (kWheelDiameter * pi) / (4 * kEncoderPPR)