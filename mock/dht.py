import random

class DHT22:
    def __init__(self, pin):
        self.temp = 25.0
        self.hum = 40.0

    def measure(self):
        # simula leitura aleatória
        self.temp = round(random.uniform(20.0, 35.0), 1)
        self.hum = round(random.uniform(20.0, 60.0), 1)

    def temperature(self):
        return self.temp

    def humidity(self):
        return self.hum
