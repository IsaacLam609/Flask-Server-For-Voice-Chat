import time

import paho.mqtt.client as mqtt

import settings

ASSISTANT_INPUT_TOPIC = "/alphamini/sendtoha"
ASSISTANT_RESPONSE_TOPIC = "/alphamini/getfromha"


def generate_response(message):
    """
    Gets a response for a given message by sending and receiving MQTT messages from Home Assistant.
    Home Assistant uses the 'extended OpenAI conversation' integration to generate the response.

    Args:
        message (str): The input message.

    Returns:
        str: The response message.
    """
    response_message = None

    # Callback functions for MQTT client
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            # print("Connected to MQTT broker!")
            client.subscribe(ASSISTANT_RESPONSE_TOPIC)
            client.publish(ASSISTANT_INPUT_TOPIC, message)
            # print("MQTT message published: ", message)
        else:
            print("Failed to connect to MQTT broker, return code:", rc)

    def on_message(client, userdata, msg):
        nonlocal response_message
        response_message = msg.payload.decode()
        print(f"Received message: {msg.payload.decode()}")
        client.loop_stop()
        client.disconnect()

    # Create MQTT client and set callbacks
    client = mqtt.Client(client_id="", userdata=None, protocol=mqtt.MQTTv311)
    client.on_connect = on_connect
    client.on_message = on_message

    # Set username and password
    client.username_pw_set(settings.BROKER_USERNAME, settings.BROKER_PASSWORD)

    # Connect to MQTT broker and publish message
    client.connect(settings.BROKER_HOST, settings.BROKER_PORT, 60)

    # Loop until we get a response
    client.loop_forever()
    return response_message
