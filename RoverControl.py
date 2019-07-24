''' RoverControl.py '''
print(" - RoverControl.py Loaded")

### This imports the library that controls the input and output pins of the Raspberry Pi board, known as the ‘general purpose input output’ pins ###
import RPi.GPIO as GPIO
import time


### I setup the Control object so that it can be called easily and more effectively as all the variables and control methods will remain in memory for the entirely of the programs runtime. This allows for the controls to be much more responsive and reduces the load on the CPU when executing a move - it just sends the command instead of having to load the entire list of variables and the functions into memory, as well as the initalisation before executing the move command ###
class Control:

    MOTOR_DELAY = 0.2

    RIGHT_PWM_PIN = 14
    RIGHT_1_PIN = 10
    RIGHT_2_PIN = 25
    LEFT_PWM_PIN = 24
    LEFT_1_PIN = 17
    LEFT_2_PIN = 4
    left_pwm = 0
    right_pwm = 0
    pwm_scale = 0

    old_left_dir = -1
    old_right_dir = -1

### This function sets up the GPIO so that it can be used with pulse width modulation, which is necessary for the proper control of the motors that I am using with the control board ###
    def __init__(self, battery_voltage=9.0, motor_voltage=6.0, revision=2):

        self.pwm_scale = float(motor_voltage) / float(battery_voltage)

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.LEFT_PWM_PIN, GPIO.OUT)
        self.left_pwm = GPIO.PWM(self.LEFT_PWM_PIN, 500)
        self.left_pwm.start(0)
        GPIO.setup(self.LEFT_1_PIN, GPIO.OUT)
        GPIO.setup(self.LEFT_2_PIN, GPIO.OUT)

        GPIO.setup(self.RIGHT_PWM_PIN, GPIO.OUT)
        self.right_pwm = GPIO.PWM(self.RIGHT_PWM_PIN, 500)
        self.right_pwm.start(0)
        GPIO.setup(self.RIGHT_1_PIN, GPIO.OUT)
        GPIO.setup(self.RIGHT_2_PIN, GPIO.OUT)

### The next 2 functions deals with getting the information from the relevant commands and executing it on the motors via the control board. It does this by calculation the PWM of the motors as well as the relevant pins based on the direction given, and sets the motors to that. As well as that, it also adds some extra features such as ensuring that the motors fully stop before switching directions suddenly to make sure that any behaviour of the motors is predictable and repeatable ###
    def set_motors(self, left_pwm, left_dir, right_pwm, right_dir):
        if self.old_left_dir != left_dir or self.old_right_dir != right_dir:
            self.set_driver_pins(0, 0, 0, 0)    # stop the motors between sudden changes of direction
            time.sleep(self.MOTOR_DELAY)
        self.set_driver_pins(left_pwm, left_dir, right_pwm, right_dir)
        self.old_left_dir = left_dir
        self.old_right_dir = right_dir

    def set_driver_pins(self, left_pwm, left_dir, right_pwm, right_dir):
        self.left_pwm.ChangeDutyCycle(left_pwm * 100 * self.pwm_scale)
        GPIO.output(self.LEFT_1_PIN, left_dir)
        GPIO.output(self.LEFT_2_PIN, not left_dir)
        self.right_pwm.ChangeDutyCycle(right_pwm * 100 * self.pwm_scale)
        GPIO.output(self.RIGHT_1_PIN, right_dir)
        GPIO.output(self.RIGHT_2_PIN, not right_dir)

### The next 5 functions are the callable functions that are used with the OOP class so that the 4 directions and the stop command are all easily callable without also having to supply the proper parameters to the command - as they are dealt with within the motor control code. This makes it a lot cleaner to write code for as well as making all of the sections of the program individual from one another. ###
    def forwards(self, seconds=0, speed=1.0):
        self.set_motors(speed, 0, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def stop(self):
        self.set_motors(0, 0, 0, 0)

    def backwards(self, seconds=0, speed=1.0):
        self.set_motors(speed, 1, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def left(self, seconds=0, speed=0.5):
        self.set_motors(speed, 0, speed, 1)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def right(self, seconds=0, speed=0.5):
        self.set_motors(speed, 1, speed, 0)
        if seconds > 0:
            time.sleep(seconds)
            self.stop()

    def cleanup(self):
        GPIO.cleanup()
