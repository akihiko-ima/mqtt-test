import paho.mqtt.client as mqtt

# メッセージ受信時のコールバック
def on_message(client, userdata, message):
    print(f"受信: {message.topic} -> {message.payload.decode()}")

# VERSION2 APIで初期化
client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("test/topic")

# 受信待ちループ
client.loop_forever()