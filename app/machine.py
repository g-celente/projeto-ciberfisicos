class Pin:
    OUT = 0

    def __init__(self, pin, mode=None):
        self.pin = pin
        self.state = False

    def on(self):
        self.state = True
        print(f"[PIN {self.pin}] ON")

    def off(self):
        self.state = False
        print(f"[PIN {self.pin}] OFF")

class PWM:
    def __init__(self, pin, freq=50):
        self.pin = pin
        self.freq = freq
        self.duty_value = 0

    def duty(self, value):
        self.duty_value = value
        print(f"[PWM PIN {self.pin.pin}] Duty set to {value}")
