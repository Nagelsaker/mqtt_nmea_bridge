import paho.mqtt.client as mqtt

def main():
    # Initialize the client.
    client = mqtt.Client()

    # Assign the callback functions.
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker.
    client.connect("localhost", 1883, 5)

    # Blocking call that processes network traffic, dispatches callbacks, and handles reconnecting.
    client.loop_forever()

# Callback when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("test/topic")

# Callback when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")

if __name__ == "__main__":
    main()