from app.dht22 import DHT22
from app.servo import Servo
from app.machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient
import ujson
import ntptime
#import paho.mqtt.client as paho
#from paho import mqtt

# --- CONFIGURAÇÕES MQTT COM HIVE MQ CLOUD ---
MQTT_BROKER = 'mqtt-dashboard.com'
MQTT_PORT = 8883
MQTT_USERNAME = ''
MQTT_PASSWORD = ''
CLIENT_ID = 'sensor-ciberfisico-python'
TOPIC = 'esp32-sensor-ciberfisico'

# --- CONFIGURAÇÃO DE WIFI --- #
SSID = 'Wokwi-GUEST'
PASSWORD = ''

def setup_mqtt():
    try:
        client = MQTTClient(
            client_id=CLIENT_ID,
            server=MQTT_BROKER,
            user=MQTT_USERNAME,
            password=MQTT_PASSWORD
        )
        client.connect()
        print("MQTT conectado com sucesso")
        return client
    except Exception as e:
        print("Erro ao conectar MQTT:", e)
        return None

def sincronizar_relogio():
    try:
        ntptime.settime()
        print("RTC sincronizado via NTP.")
    except Exception as e:
        print("Erro ao sincronizar RTC:", e)

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
    print('Wi-Fi conectado:', wlan.ifconfig())

def log(msg):
    with open('log.txt', 'a') as f:
        f.write(f"{time.time()}: {msg}\n")

def formatar_data_hora():
    t = time.localtime()
    data = f"{t[2]:02d}/{t[1]:02d}/{t[0]}"
    horario = f"{t[3]:02d}h{t[4]:02d}"
    return data, horario

def main():
    conectar_wifi()
    sincronizar_relogio()
    mqtt = setup_mqtt()

    sensor = DHT22(15)
    servo = Servo(2)
    vibracao = Pin(27, Pin.IN)
    corrente = ADC(Pin(34))
    corrente.atten(ADC.ATTN_11DB)
    gas = ADC(Pin(32))  # novo sensor de gás
    gas.atten(ADC.ATTN_11DB)
    luminosidade = ADC(Pin(33))  # novo sensor de luminosidade
    luminosidade.atten(ADC.ATTN_11DB)

    umidade_minima = 60

    while True:
        temp = sensor.temperatura()
        umid = sensor.umidade()
        vibra = vibracao.value()
        corr = corrente.read()
        gas_valor = gas.read()
        luz_valor = luminosidade.read()
        data, horario = formatar_data_hora()

        if umid is not None:
            if umid < umidade_minima:
                if servo.angle != 0:
                    servo.set(0)
                irrigacao_status = "ativada"
            else:
                if servo.angle != 90:
                    servo.set(90)
                irrigacao_status = "desativada"

            json_payload = {
                "temp": f"{temp}c",
                "umidade": f"{umid}%",
                "vibracao": str(vibra),
                "corrente": f"{corr}v",
                "gas": str(gas_valor),
                "luminosidade": str(luz_valor),
                "irrigacao": irrigacao_status,
                "data": data,
                "horario": horario
            }

            print(json_payload)
            log(str(json_payload))

            if mqtt:
                try:
                    mqtt.publish(TOPIC, ujson.dumps(json_payload))
                except Exception as e:
                    print("Erro ao publicar MQTT:", e)
                    log("Erro ao publicar MQTT")

        else:
            print("Erro ao ler sensores. Tentando novamente...")
            log("Erro ao ler sensores.")

        time.sleep(2)

if __name__ == "__main__":
    main()
