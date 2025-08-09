# 概要
本リポジトリは、MQTT 通信テスト用のリポジトリです

# 環境
- Mosquitto（MQTTブローカー）をインストール
```bash
sudo apt install mosquitto mosquitto-clients -y
```
- Mosquitto（MQTTブローカー）の起動
```bash
sudo systemctl start mosquitto
```

## テストコード実行コマンド
#### Publisher
```bash
uv run src/publisher.py
```
#### Subscriber
```bash
uv run src/subscriber.py
```