import sys
import signal
import tomllib
import paho.mqtt.client as mqtt


CONFIG_PATH = "config.toml"
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)


def on_connect(client, userdata, flags, reason_code, properties):
    """MQTTブローカーへの接続時に呼ばれるコールバック"""
    if reason_code == 0:
        print("接続成功")
    else:
        print(f"接続失敗: reason_code={reason_code}")


def on_message(client, userdata, msg):
    """メッセージ受信時に呼ばれるコールバック"""
    print(f"TOPIC: {msg.topic}, QOS: {msg.qos}, PAYLOAD: {msg.payload.decode('utf-8')}")


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    """サブスクライブ完了時に呼ばれるコールバック"""
    print(f"Subscribed: mid={mid}, reason_code_list={reason_code_list}")


def signal_handler(sig, frame):
    """Ctrl+C時の切断処理"""
    print("\nCtrl+C検知。MQTT切断処理を実行します。")
    client.disconnect()
    client.loop_stop()
    sys.exit(0)


if __name__ == "__main__":
    try:
        client = mqtt.Client(
            client_id=config["mqtt"]["sub_client_id"],
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_subscribe = on_subscribe

        signal.signal(signal.SIGINT, signal_handler)

        client.connect(
            host=config["mqtt"]["broker_ip_addr"],
            port=config["mqtt"]["port"],
            keepalive=config["mqtt"]["max_second_conect"],
        )
        client.subscribe(config["mqtt"]["sub_topic"])
        client.loop_forever()
    except Exception as e:
        print(f"エラー発生: {e}")
        sys.exit(1)
