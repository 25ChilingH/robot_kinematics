import time  # used to set delay time to control moving distance
import sys  # used for command line options
import busio
from adafruit_pca9685 import PCA9685
import utils
from Robot import Robot
import matplotlib.pyplot as plt
from mpu6050 import mpu6050

# set up Raspberry Pi GPIO
import RPi.GPIO as GPIO  # control through GPIO pins

robot = Robot()
# set up PC9685 osoyoo/AdaFruit
# from board import SCL,SDA
SCL = 3
SDA = 2

# adafruit forces GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BCM)
# I2C for PCS9685 and Gyro
# create i2c bus interface to access PCA9685, for example
i2c = busio.I2C(SCL, SDA)  # busio.I2C(board.SCL, board.SDA) create i2c bus
pca = PCA9685(i2c)  # adafruit_pca9685.PCA9685(i2c)   instance PCA9685 on bus
# pca = PCA9685()   # adafruit_pca9685.PCA9685(i2c)   instance PCA9685 on bus
pca.frequency = 1000  # set pwm clock in Hz (debug 60 was 1000)
# usage: pwm_channel = pca.channels[0] instance example
#        pwm_channel.duty_cycle = speed (0 .. 100)  speed example


# motors
# front controller, PCA channel
ENAFR = 0
IN1FR = 1
IN2FR = 2

IN3FL = 5
IN4FL = 6
ENBFL = 4
# rear controller, PCA channel
ENARR = 8
IN1RR = 9
IN2RR = 10

IN3RL = 13
IN4RL = 14
ENBRL = 12

# Encoders, GPIO.board pin
S1FR = 17  # pin 11
S2FR = 27  # pin 13

S1FL = 22  # pin 15
S2FL = 10  # pin 19

S1RR = 9  # pin 21
S2RR = 11  # pin 23

S1RL = 5  # pin 29
S2RL = 6  # pin 31
perRev = 749  # estimate A type motors

# PCA9685
PWMOEN = 4  # pin 7 # PCA9685 OEn pin
pwmOEn = GPIO.setup(PWMOEN, GPIO.OUT)  # enable PCA outputs

# push button
pushButton = 26  # pin 37, GPIO 26
GPIO.setup(pushButton, GPIO.IN)
oldPushb = 0


def readPush():
    global oldPushb
    pushb = GPIO.input(pushButton)
    if pushb != oldPushb:
        oldPushb = pushb
        return True, pushb
    else:
        return False, pushb


# GPIO.setup(outputPIN, GPIO.OUT)
# GPIO.setup(inputPIN, GPIO.IN)
# GPIO.output(outputPIN) = write
# read = GPIO.input(inputPIN)
# PWM RPi 4 has two channels, but each can be used twice
# PWM channel 0 on pin 32 = pin 12; PWM channel 0 on pin 33 = pin 35
# PWM create & start each pin
# pwm = GPIO.PWM(pwmPIN,1000)  creates instance, where 1000 is the base frequency
# channel alternate, uses same frequency (or overrides for both channels)
# pwm.start(speed)             starts and sets speed, where speed can be >= 0 up to 4095
# channel alternate, uses same frequency (or overrides for both channels)


# equivalent of Arduino map()
def valmap(value, istart, istop, ostart, ostop):
    return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))


# for 0 to 100, % speed as integer, to use for PWM
# full range 0xFFFF, but PCS9685 ignores last Hex digit as only 12 bit resolution)
def getPWMPer(value):
    return int(valmap(value, 0, 100, 0, 0xFFFF))


# for IN1, IN2, define 1  and 0 settings
high = 0xFFFF  # 1 was True
low = 0  # 0 was False


class Wheel:
    def __init__(self, name, enCh, in1Ch, in2Ch):
        self.name = name  # for debug
        self.en = pca.channels[enCh]  # EN  wheel 'speed', actually sets power
        self.in1 = pca.channels[in1Ch]  # IN1, IN3 wheel direction control 1
        self.in2 = pca.channels[in2Ch]  # IN2, IN4 wheel direction control 2
        self.pidController = utils.initPIDController(robot.delay)
        # If IN1=True  and IN2=False motor moves forward,
        # If IN1=False and IN2=True  motor moves backward
        # in both other cases motor will stop/brake
        # right: ENA, IN1, IN2
        # left:  ENB, IN3, IN4 - IN1=IN4 and IN2=IN3 but motor is reversed, so swap

        # print("created Wheel "+str(self.name)+" at "+str(enCh)+" "+str(in1Ch)+" "+str(in2Ch)) #debug

    def move(self, power):
        self.in1.duty_cycle = high if power > 0 else low
        self.in2.duty_cycle = low if power > 0 else high
        self.en.duty_cycle = getPWMPer(power) if power > 0 else getPWMPer(-power)
        # print("move "+self.name+" @ "+str(power)) # debug
        # positive power forward, negative power reverse/back; 0 = coast, 100% = 4095

    def brake(self):
        self.in1.duty_cycle = low
        self.in2.duty_cycle = low
        # print("brake "+self.name) #debug
        # electric braking effect, should stop movement


# end of Wheel class

# Set up Wheel instances with connections, ch 0 is left end,
# leaving one pin per quad for future
rl = Wheel("rl", ENBRL, IN3RL, IN4RL)  # Rear-left wheel
rr = Wheel("rr", ENARR, IN1RR, IN2RR)  # Rear-right wheel
fl = Wheel("fl", ENBFL, IN3FL, IN4FL)  # Front-left wheel
fr = Wheel("fr", ENAFR, IN1FR, IN2FR)  # Front-right wheel


# encoder class
class Encoder:
    def __init__(self, name, S1, S2, side):
        self.name = name  # for debug
        self.s1 = S1  # pin
        GPIO.setup(S1, GPIO.IN)  # instance
        self.s2 = S2  # pin
        GPIO.setup(S2, GPIO.IN)
        self.aState = 0  # value (aState)
        self.bState = 0
        self.aLastState = 0  # remember last value (aLastState)
        self.bLastState = 0  # not needed?
        self.counter = 0
        self.lastCounter = 0
        self.aturn = 0  # for diagnostic
        self.bturn = 0  # for diagnostic
        self.speed = 0
        self.time = time.perf_counter_ns()
        self.lastTime = self.time
        self.side = side

    def read(self):
        self.aState = GPIO.input(self.s1)
        self.bState = GPIO.input(self.s2)
        self.time = time.perf_counter_ns()
        return self.aState, self.bState

    def read_turn(self):
        return self.aturn, self.bturn  # for diagnostic (whole method)

    def read_name(self):
        return self.name  # for diagnostic (whole method)

    def readEncoder(self):
        # Reads the "current" state of the encoders
        aState, bState = self.read()
        # If the previous and the current state are different,  a Pulse has occured
        if aState != self.aLastState:
            # self.aturn +=1; #for diagnostic
            # If the outputB state is different to the outputA state, rotating clockwise
            if bState != aState:
                self.counter += 1
            else:  # rotating counter clockwise
                self.counter -= 1

        if bState != self.bLastState:
            self.bturn += 1
            # for diagnostic

        # if aState != self.aLastState or bState != self.bLastState:
        # print(self.name +" position: " + str(self.counter) + " a: " + str(self.aturn) + " b: " + str(self.bturn) ) #for diagnostic

        self.aLastState = aState  # remember last state of a
        self.bLastState = bState  # remember last state of b (for diagnostic)

    def readEncoderTest(self):
        self.readEncoder()
        # print(self.name +" position: " + str(self.counter)  ) #for diagnostic

    # set up call back functions, ignore 2nd parameter
    def callback_encoder(self, channel):
        self.readEncoder()

    def readSpeed(self):
        # correct for side of car left goes - otherwise
        if self.time != 0 and self.time != self.lastTime:  # store speed in clicks/nS
            self.speed = (
                self.side
                * (self.counter - self.lastCounter)
                / (self.time - self.lastTime)
            )
        else:
            self.speed = 0

        # lastTime and lastCounter were set at last call to this function
        self.lastTime = self.time  # time was set at each/last call to .read
        self.lastCounter = (
            self.counter
        )  # counter was set at each/last call to .readEncoder

        # print(self.name +" position: " + str(self.counter) + " @: " + str(self.time) + \
        #   " speed rev/sec: " + str(self.speed*1E9/perRev) ) #for diagnostic
        # print counts revs /second
        return self.speed * 1e9 / perRev * utils.rotsToMeters()

    def resetSpeed(self):
        self.speed = 0
        self.counter = 0
        self.lastCounter = 0
        # may need initialize since stop so 1st speed valid
        self.time = self.lastTime = time.perf_counter_ns()


# end of Encoder class

# Set up Encoder instances with connections, GPIO.board (swheel),
# right side = -1 if forward speed reported negative
# left side  =  1
sfl = Encoder("sfl", S1FL, S2FL, 1)
sfr = Encoder("sfr", S1FR, S2FR, -1)
srl = Encoder("srl", S1RL, S2RL, 1)
srr = Encoder("srr", S1RR, S2RR, -1)


def test_speed():
    print("fl: ", sfl.readSpeed())
    print("fr: ", sfr.readSpeed())
    print("rl: ", srl.readSpeed())
    print("rr: ", srr.readSpeed())


def test_Encoders():
    sfl.readEncoderTest()
    sfr.readEncoderTest()
    srl.readEncoderTest()
    srr.readEncoderTest()


# set up call back functions, ignore parameter and unique
# def callback_sfl(channel):
#  sfl.readEncoder()


# set up interrupts on A encoders, channel needs GPIO channel,
# callback has no parameters defined here,
#  automatically gets self if object, + channel
GPIO.add_event_detect(sfl.s1, GPIO.BOTH, callback=sfl.callback_encoder)
GPIO.add_event_detect(sfr.s1, GPIO.BOTH, callback=sfr.callback_encoder)
GPIO.add_event_detect(srl.s1, GPIO.BOTH, callback=srl.callback_encoder)
GPIO.add_event_detect(srr.s1, GPIO.BOTH, callback=srr.callback_encoder)


class Gyro:
    def __init__(self):
        self.sensor = mpu6050(0x68)
        self.yawTime = time.perf_counter_ns()
        self.lastYawTime = self.yawTime

    # in g's
    def readAccX(self):
        accel_data = self.sensor.get_accel_data()
        return accel_data["x"]

    # in g's
    def readAccY(self):
        accel_data = self.sensor.get_accel_data()
        return accel_data["y"]

    # CCW+ deg/s
    def readYawSpeed(self):
        gyro_data = self.sensor.get_gyro_data()
        self.yawTime = time.perf_counter_ns()
        return gyro_data["z"]

    # def readYaw(self):
    #     yawSpeed = self.readYawSpeed()
    #     if self.yawTime != 0 and self.yawTime != self.lastYawTime:
    #         return yawSpeed * (self.yawTime - self.lastYawTime) / 1e9
    #     self.lastYawTime = self.yawTime


gyro = Gyro()

# Movement control examples
# rear right motor moving forward was def rr_ahead(speed): ... now rr.move(speed)
# rear right motor moving back    was def rr_back(speed): ...  now rr.move(-speed)


def stop_car():  # brakes all 4 wheels
    rl.brake()
    rr.brake()
    fl.brake()
    fr.brake()
    time.sleep(1)  # allow time to halt, then reset all speeds to 0
    sfl.resetSpeed()
    srr.resetSpeed()
    srl.resetSpeed()
    sfr.resetSpeed()
    # note may need to resetSpeed at start of a new action, *** to check if needed
    #      coast does not reset speed, deliberately, as car may still move.


def go_ahead(power, forSecs):
    rl.move(power)
    rr.move(power)
    fl.move(power)
    fr.move(power)
    time.sleep(forSecs)


def go_back(power, forSecs):
    rr.move(-power)
    rl.move(-power)
    fr.move(-power)
    fl.move(-power)
    time.sleep(forSecs)


def computeSpeed(i):
    if robot.drive == "tank":
        wheelSpeeds = utils.computeTankWheelSpeed(
            robot.pltPoints[i],
            robot.pltPoints[utils.nexti(i, len(robot.pltPoints))],
            robot.delay,
            robot.robotWidth,
            robot.robotLength,
        )
    elif robot.drive == "mecanum":
        wheelSpeeds = utils.computeWheelSpeed(
            robot.pltPoints[i],
            robot.pltPoints[utils.nexti(i, len(robot.pltPoints))],
            robot.delay,
            robot.robotWidth,
            robot.robotLength,
        )
    return wheelSpeeds


def plotPID(times, setpoints, measurement):
    fig, ax = plt.subplots()
    ax.plot(times, setpoints[0], "ro")
    ax.plot(times, measurement[0], "bo")
    plt.show()


def follow_shape(scale):
    encoders = [sfl, sfr, srl, srr]
    motors = [fl, fr, rl, rr]
    pidControllers = [
        fl.pidController,
        fr.pidController,
        rl.pidController,
        rr.pidController,
    ]
    setpoints = [[] for x in range(4)]
    measure = [[] for x in range(4)]
    times = []
    for i in range(len(robot.pltPoints)):
        wheelSpeeds = computeSpeed(i)
        times.append(i)
        for wheelIdx in range(4):
            setpoint = wheelSpeeds[wheelIdx] * scale
            pidControllers[wheelIdx].setpoint = setpoint
            speed = encoders[wheelIdx].readSpeed()
            power = utils.getWheelPower(pidControllers[wheelIdx](speed), wheelIdx)
            setpoints[wheelIdx].append(setpoint)
            measure[wheelIdx].append(speed)
            print(wheelIdx, setpoint, speed, power)
            motors[wheelIdx].move(power)
        time.sleep(robot.delay)
    stop_car()
    plotPID(times, setpoints, measure)


def arc_left(power, forSecs):
    rr.move(power)
    rl.move(power * 0.5)
    fr.move(power)
    fl.move(power * 0.5)
    time.sleep(forSecs)


# making right turn on spot (tank turn)
def turn_right(power, forSecs):
    rl.move(power)
    rr.move(-power)
    fl.move(power)
    fr.move(-power)
    time.sleep(forSecs)


# make left turn on spot (tank turn)
def turn_left(power, forSecs):
    rr.move(power)
    rl.move(-power)
    fr.move(power)
    fl.move(-power)
    time.sleep(forSecs)


# parallel left shift (crab left)
def shift_left(power, forSecs):
    fr.move(power)
    rr.move(-power)
    rl.move(power)
    fl.move(-power)
    time.sleep(forSecs)


# parallel right shift (crab right)
def shift_right(power, forSecs):
    fr.move(-power)
    rr.move(power)
    rl.move(-power)
    fl.move(power)
    time.sleep(forSecs)


# diagonal forward and right @45
def upper_right(power, forSecs):
    rr.move(power)
    fl.move(power)
    time.sleep(forSecs)


# diagonal back and left @45
def lower_left(power, forSecs):
    rr.move(-power)
    fl.move(-power)
    time.sleep(forSecs)


# diagonal forward and left @45
def upper_left(power, forSecs):
    fr.move(power)
    rl.move(power)
    time.sleep(forSecs)


# diagonal back and right @45
def lower_right(power, forSecs):
    fr.move(-power)
    rl.move(-power)
    time.sleep(forSecs)


# front left only
def front_left(power, forSecs):
    print("Front left ahead @ " + str(power) + "% for " + str(forSecs) + " secs.")
    fl.move(power)
    time.sleep(forSecs)
    test_speed()
    stop_car()  # will set speed to 0


# front right only
def front_right(power, forSecs):
    print("Front right ahead @ " + str(power) + "% for " + str(forSecs) + " secs.")
    fr.move(power)
    time.sleep(forSecs)
    test_speed()
    stop_car()  # will set speed to 0


# rear left only
def rear_left(power, forSecs):
    print("Rear left ahead @ " + str(power) + "% for " + str(forSecs) + " secs.")
    rl.move(power)
    time.sleep(forSecs)
    test_speed()
    stop_car()  # will set speed to 0


# rear right only
def rear_right(power, forSecs):
    print("Rear right ahead @ " + str(power) + "% for " + str(forSecs) + " secs.")
    rr.move(power)
    time.sleep(forSecs)
    test_speed()
    stop_car()  # will set speed to 0


def coastAll(forSecs):
    print("Coast forSecs " + str(forSecs) + " secs.")
    rl.move(0)
    rr.move(0)
    fr.move(0)
    rr.move(0)
    time.sleep(forSecs)
    stop_car()  # will set speed to 0


def test_move():
    # pwmOEn=0 # enable outputs of PCA9685
    # GPIO.output(outputPIN) = write
    GPIO.output(PWMOEN, 1)
    print("By wheel")
    time.sleep(2)  # for operator

    front_left(100, 2)
    time.sleep(3)  # for operators benefit
    front_right(100, 2)
    time.sleep(3)  # for operators benefit
    rear_left(100, 2)
    time.sleep(3)  # for operators benefit
    rear_right(100, 2)
    time.sleep(3)  # for operators benefit

    print("Run forward all, full power for 1 sec, then coast all for 3 sec, then stop")
    rl.move(100)
    rr.move(100)
    fl.move(100)
    rr.move(100)
    time.sleep(1)
    rl.move(0)
    rr.move(0)
    fl.move(0)
    rr.move(0)
    time.sleep(3)
    stop_car()  # will reset speed
    print("Stopped and speed reset")


def test_gyro():
    while True:
        print(
            "Yaw Speed:",
            gyro.readYawSpeed(),
            "AccX:",
            gyro.readAccX(),
            "AccY:",
            gyro.readAccY(),
        )
        time.sleep(0.5)


# def test_readYaw():
#     yaw = gyro.readYaw()
#     time.sleep(0.5)
#     print("Yaw in degs:", yaw)


def test_readPush():
    changed, state = readPush()
    if changed:
        print("button changed to " + str(state))


def destroy():
    # pwmOEn=1 # disable outputs of PCA9685
    GPIO.output(PWMOEN, 1)
    GPIO.cleanup()


def Robot():
    print("starting main, using file list of functions")
    dir = "./instructions/"
    if len(sys.argv) == 1:
        myfile = dir + "square.txt"
    else:
        myfile = sys.argv[1]
    print("reading file ", myfile)

    with open(myfile, encoding="utf-8") as myf:
        actionList = myf.readlines()

    # actionList=[front_left(100,2),front_right(100,2),rear_left(100,2),rear_right(100,2)]
    GPIO.output(PWMOEN, 0)  # enable PWM outputs
    for x in actionList:
        print(x, end="")
        if "#" not in x:
            exec(x)
    stop_car()  # stop movement
    destroy()  # clean up GPIO
    print("\nStopped and cleanup done")

    # test_readPush()
    # test_move()
    # test_Encoders()


if __name__ == "__main__":
    try:
        Robot()
    except KeyboardInterrupt:
        # press ctrl-C
        stop_car()  # stop movement
        destroy()  # clean up GPIO
        print("\nStopped and cleanup done")
