import paho.mqtt.client as mqtt
import time

def main():
    # Initialize the client.
    client = mqtt.Client()

    # Assign the callback function.
    client.on_connect = on_connect

    # Connect to the broker.
    client.connect("localhost", 1883, 5)
    client.loop_start()

    message = "Hellow, World!"
    topic = "test/topic"
    
    t = 100
    while t > 0:
        client.publish(f"{topic}", f"{message}")
        time.sleep(1)
        t -= 1

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")

if __name__ == "__main__":
    main()