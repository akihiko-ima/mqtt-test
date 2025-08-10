import sys
import signal
import time
import tomllib
import paho.mqtt.client as mqtt


CONFIG_PATH = "config.toml"
with open(CONFIG_PATH, "rb") as f:
    config = tomllib.load(f)


def on_connect(client, userdata, flags, reason_code, properties):
    """MQTT接続時に呼ばれるコールバック（v2仕様）"""
    if reason_code == 0:
        print("接続成功")
    else:
        print(f"接続失敗: reason_code={reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    """MQTT切断時に呼ばれるコールバック（v2仕様）"""
    if reason_code != 0:
        print(f"予期しない切断: reason_code={reason_code}")


def on_publish(client, userdata, mid, reason_code, properties):
    """メッセージ送信完了時に呼ばれるコールバック（v2仕様）"""
    print(f"message_id={mid}, reason_code={reason_code}")


def signal_handler(sig, frame):
    """Ctrl+C時の切断処理"""
    print("\nCtrl+C検知。MQTT切断処理を実行します。")
    client.disconnect()
    client.loop_stop()
    sys.exit(0)


if __name__ == "__main__":
    try:
        client = mqtt.Client(
            client_id=config["mqtt"]["pub_client_id"],
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        )
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        client.on_publish = on_publish

        signal.signal(signal.SIGINT, signal_handler)

        client.connect(
            host=config["mqtt"]["broker_ip_addr"],
            port=config["mqtt"]["port"],
            keepalive=config["mqtt"]["max_second_conect"],
        )
        client.loop_start()

        i = 0
        while True:
            result = client.publish(
                topic=config["mqtt"]["pub_topic"],
                payload=f"Hello!! {i} time",
                qos=config["mqtt"]["qos"],
            )
            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                print(f"Publish failed: {result.rc}")
            i += 1
            time.sleep(1)
    except Exception as e:
        print(f"エラー発生: {e}")
        sys.exit(1)
