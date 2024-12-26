import RPi.GPIO as GPIO
import tm1637


class RGBLed:
    def __init__(self, red_pin, green_pin):
        """
        Initialize the RGB LED with red and green pins.

        :param red_pin: GPIO pin connected to the red channel.
        :param green_pin: GPIO pin connected to the green channel.
        """
        self.red_pin = red_pin
        self.green_pin = green_pin

        GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering
        GPIO.setup(self.red_pin, GPIO.OUT)
        GPIO.setup(self.green_pin, GPIO.OUT)

        # Set up PWM for red and green pins (50Hz frequency)
        self.red_pwm = GPIO.PWM(self.red_pin, 50)
        self.green_pwm = GPIO.PWM(self.green_pin, 50)

        # Start PWM with 0% duty cycle (off)
        self.red_pwm.start(0)
        self.green_pwm.start(0)

    def set_color(self, red_value, green_value):
        """
        Set the brightness of the red and green channels.

        :param red_value: Brightness of red channel (0-100).
        :param green_value: Brightness of green channel (0-100).
        """
        if not (0 <= red_value <= 100 and 0 <= green_value <= 100):
            raise ValueError("Color values must be between 0 and 100.")

        self.red_pwm.ChangeDutyCycle(red_value)
        self.green_pwm.ChangeDutyCycle(green_value)

    def go_green(self):
        """
        Set the light to green (0/100)
        """
        print("going green")
        self.red_pwm.ChangeDutyCycle(100)
        self.green_pwm.ChangeDutyCycle(0)

    def go_yellow(self):
        """
        Set the light to yellow (50/50)
        """
        print("going yellow")
        self.red_pwm.ChangeDutyCycle(40)
        self.green_pwm.ChangeDutyCycle(70)

    def go_red(self):
        """
        Set the light to red (100/0)
        """
        print("going red")
        self.red_pwm.ChangeDutyCycle(0)
        self.green_pwm.ChangeDutyCycle(100)


class Prayer:
    def __init__(self, clk, dio, red, green) -> None:
        self.time = tm1637.TM1637(clk=clk, dio=dio)
        self.time.numbers(clk, dio)
        self.light = RGBLed(red, green)
        self.light.go_red()

    def set_time(self, time):
        self.time.numbers(time.hour, time.minute)

    def red(self):
        self.light.go_red()

    def green(self):
        self.light.go_green()

    def yellow(self):
        self.light.go_yellow()


def cleanup():
    GPIO.cleanup()
