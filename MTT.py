import time
import paho.mqtt.client as mqtt
from counterfit_shims_grove.devices import DHT

sensor = DHT('0')
broker_address = "test.mosquitto.org" 
client = mqtt.Client("SensorSimulator")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectar a broker")
    else:
        print("Conneccion fallida")

client.on_connect = on_connect

client.connect(broker_address)

client.loop_start()

try:
    while True:
    
        sensor.read()
        temperature = sensor.temperature
        humidity = sensor.humidity
        payload = f"{{'temperature': {temperature}, 'humidity': {humidity}}}"
        client.publish("sensor/temperature", temperature)
        client.publish("sensor/humidity", humidity)

        print(f"Published temperature: {temperature} and humidity: {humidity}")
        time.sleep(5)

except KeyboardInterrupt:
    print("Simulation stopped")
finally:
    client.loop_stop()
    client.disconnect()

