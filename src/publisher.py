import paho.mqtt.client as mqtt
import time

# VERSION2 APIで初期化
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

client.connect("localhost", 1883, 60)

for i in range(10):
    message = f"Hello MQTT {i}"
    client.publish("test/topic", message)
    print(f"送信: {message}")
    time.sleep(1)

client.disconnect()