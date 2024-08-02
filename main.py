from flask import Flask, request
import paho.mqtt.client as mqtt
import whisper

stt_model = whisper.load_model("large-v3", device="cuda")    # use cpu for device if no gpu available
app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def speech_to_text():
    with open("my.wav", 'wb') as f:
        f.write(request.data)

    # speech to text
    print("Start speech to text")
    result = stt_model.transcribe(audio="my.wav", language="yue")
    text = result["text"]
    print(text)

    # send mqtt message
    if text == " 我想開燈":
        mqtt_publish("/airlab/light/W402e", "On")
    elif text == " 我想熄燈":
        mqtt_publish("/airlab/light/W402e", "Off")

    return "File uploaded successfully", 200


def mqtt_publish(topic, message):
    # MQTT broker details
    BROKER_HOST = "your-broker-url"  # Tailscale ipv4
    BROKER_PORT = "your-port"              # default mqtt port
    BROKER_USERNAME = "your-username"
    BROKER_PASSWORD = "your-password"

    # Callback functions for MQTT client
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker!")
            client.subscribe(topic)
        else:
            print("Failed to connect to MQTT broker, return code:", rc)

    # def on_message(client, userdata, msg):
    #     print(f"Received message: {msg.payload.decode()}")

    # Create MQTT client and set callbacks
    client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    # client.on_message = on_message

    # Set username and password
    client.username_pw_set(BROKER_USERNAME, BROKER_PASSWORD)

    # Connect to MQTT broker and publish message
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.publish(topic, message)
    print("MQTT message published")
    client.disconnect()
    # client.loop_forever()

if __name__ == '__main__':
    print(f"Model is using device: {next(stt_model.parameters()).device}")
    app.run("0.0.0.0")