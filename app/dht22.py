try:
    from machine import Pin
    import mock.dht
except ImportError:
    from app.machine import Pin
    import mock.dht as dht

class DHT22:
    def __init__(self, pin):
        self.sensor = dht.DHT22(Pin(pin))
    
    def temperatura(self):
        self.sensor.measure()
        return self.sensor.temperature()

    def umidade(self):
        self.sensor.measure()
        return self.sensor.humidity()
