import paho.mqtt.client as mqtt


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