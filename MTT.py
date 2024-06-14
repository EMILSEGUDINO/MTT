import time
import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.devices import DHT
import json


CounterFitConnection.init('localhost', 5000)


sensor = DHT('11', 0)


broker_address = "test.mosquitto.org"  
client = mqtt.Client("SensorSimulator")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado al broker")
    else:
        print("Conexión fallida con código", rc)

client.on_connect = on_connect

client.connect(broker_address)

client.loop_start()

try:
    while True:
        # Leer valores del sensor simulado
        sensor.read()
        temperature = sensor.temperature
        humidity = sensor.humidity

        # Crear el payload
        payload = {
            'temperature': temperature,
            'humidity': humidity
        }
        payload_str = json.dumps(payload)

        # Publicar los datos en los tópicos MQTT
        client.publish("sensor/temperature", temperature)
        client.publish("sensor/humidity", humidity)

        print(f"La temperatura es: {temperature} y la humedad es: {humidity}")

        time.sleep(5)

except KeyboardInterrupt:
    print("Simulación detenida")
finally:
    client.loop_stop()
    client.disconnect()


