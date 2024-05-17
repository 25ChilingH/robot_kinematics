# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Author: Chiling Han & Sania Gupta
# Both members split the work fairly evenly and then worked together on tuning the results

import time

# set up PC9685 osoyoo/AdaFruit
# from board import SCL,SDA
SCL = 3
SDA = 2

import busio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685


# equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


i2c = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c, address=0x41)
# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
pca.frequency = 50

# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2350)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=400, max_pulse=2400)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Micro servo - TowerPro SG-92R: https://www.adafruit.com/product/169
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2400)


# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo7 = servo.Servo(pca.channels[7], actuation_range=135)
class Arm:
    armJoint = [0, 0, 0, 0, 0]

    def __init__(self):
        for i in range(0, len(self.armJoint)):
            self.armJoint[i] = servo.Servo(
                pca.channels[i], min_pulse=512, max_pulse=2560, actuation_range=180
            )

    # Reset the arm to a zero position
    def zero(self):
        # We sleep in the loops to give the servo time to move into position.
        # s0 -> +L; s1 -> -D; s2 -> +D; s3 -> +R; s4 -> +close
        zeroPos = [55, 157, 120, 145, 50]
        for i in range(len(self.armJoint)):
            self.armJoint[i].angle = zeroPos[i]

        time.sleep(1.0)

    # Reset the claw to a zero position
    def resetClaw(self):
        self.armJoint[4].angle = 50
        time.sleep(1.0)

        self.armJoint[3].angle = 145
        time.sleep(1.0)

    # Close the claw
    def closeClaw(self):
        self.armJoint[4].angle = 110
        time.sleep(1.0)

    # Move the arm backwards so that the claw remains parallel to the floor
    def moveBack(self):
        threshold = 180
        while self.armJoint[1].angle < threshold:
            try:
                self.armJoint[1].angle += 0.5
            except:
                break
            self.armJoint[2].angle += 0.8
            self.armJoint[3].angle -= 2.0

            time.sleep(0.03)

    # Rotate the claw to spin the nut
    def spinClaw(self):
        threshold = 10
        while self.armJoint[3].angle > threshold:
            try:
                self.armJoint[3].angle -= 1.0
            except:
                break

            time.sleep(0.03)

    # Open the claw to drop the nut
    def dropNut(self):
        self.armJoint[4].angle = 60
        time.sleep(1.0)

    # Move the arm to the nail's position
    def moveToNail(self):
        self.armJoint[3].angle = 90
        time.sleep(1.0)
        self.armJoint[0].angle = 140
        time.sleep(1.0)
        self.armJoint[2].angle = 180
        time.sleep(1.0)

        threshold = 110
        while self.armJoint[1].angle > threshold:
            try:
                self.armJoint[1].angle -= 1.0
            except:
                break
            time.sleep(0.03)

if __name__ == "__main__":
    arm = Arm()
    arm.zero()

    NO_TURNS = 9
    print(NO_TURNS)
    for i in range(NO_TURNS):
        arm.closeClaw()
        arm.spinClaw()
        arm.resetClaw()
        print(i, "th iteration")
    arm.closeClaw()
    arm.moveBack()

    arm.moveToNail()
    arm.dropNut()

    pca.deinit()