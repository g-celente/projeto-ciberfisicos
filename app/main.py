from app.dht22 import DHT22
from app.servo import Servo 
from machine import Pin 
import time
from iot_data_hub import IoTDataHub


sensor = DHT22(15)
servo = Servo(2)
vermelho=Pin(0,Pin.OUT)



# def mensagem(topico, valor):
#     if topico == 'led':
#         if valor == 'true':
#             # servo.set(90)
#             vermelho.on()
#             print('Irrigação ligada.')
        
#         else:
#             servo.set(0)
#             vermelho.off() 
#             print('Irrigação Desligada.')   

servidor = IoTDataHub(
    'Wokwi-GUEST',
    '',
    'DQMe19JOww',
    # mensagem,
    # verbose=True
)

# servidor.subscribe('led')

x=-1
while True:

    temp = sensor.temperatura()
    servidor.publish('Temperatura',str(temp))

    umid = sensor.umidade()
    servidor.publish('Umidade',str(umid))

    if umid >= 30:
        servo.set(0)
        vermelho.off()
        if x!=0:
            print('Irrigacao Desligada')
            x=0

    else:
        servo.set(90)
        vermelho.on()
        if x!=1:
            print('Irrigacao Ligada')
            x=1

    print(f"U={umid}%")
    time.sleep(3)
        

