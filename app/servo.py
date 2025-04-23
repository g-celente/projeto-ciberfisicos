try:
    from machine import Pin, PWM
except ImportError:
    from app.machine import Pin, PWM

class Servo:
    def __init__(self, pin, angle = 0):
        self.pin = pin
        self.angle = angle
        self.motor = PWM(Pin(pin,Pin.OUT), freq=50)

    def set(self, angle):
        self.angle = 28 + (int)((124-28)*angle/180.0)
        self.motor.duty(self.angle)
