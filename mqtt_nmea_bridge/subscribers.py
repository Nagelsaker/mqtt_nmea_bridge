# MIT License
# Copyright (c) 2023 Simon J. N. Lexau
#
# --------------------------------------------------------------------------------
#
# Norwegian University of Science and Technology (NTNU)
# Department of Engineering Cybernetics
# Author: Simon J. N. Lexau
#
# --------------------------------------------------------------------------------
#
# See the LICENSE file in the project root for full license information.
#
# --------------------------------------------------------------------------------
#
import paho.mqtt.client as mqtt
import mqtt_nmea_bridge as mnb
from queue import Queue


class Subscriber:
    '''
    Subscriber client parent class for subscribing to topics from an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def __init__(self, client_id, broker, port):
        self.client = mqtt.Client(client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.broker = broker
        self.port = port
        self.queue = Queue()

    def connect(self, username, password):
        self.client.username_pw_set(f"{username}", f"{password}")
        self.client.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
        else:
            print(f"Connect failed with return code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
        
    def loop_start(self):
        self.client.loop_start()
    
    def loop_stop(self):
        self.client.loop_stop()
    
    def get(self):
        '''
        Return a dataclass object from the queue, if any is present, return 0 otherwise.
        '''
        if not self.queue.empty():
            return self.queue.get()
        else:
            return 0


class TrajectorySubscriber(Subscriber):
    '''
    Client class for subscribing to trajectories from an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def on_connect(self, client, userdata, flags, rc):
        topic = "trajectory/topic"
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            client.subscribe(topic)
            print(f"Subscribed to topic '{topic}'")

    def on_message(self, client, userdata, msg):
        # Convert NMEA string to Trajectory object
        nmea_cus_traj = msg.payload.decode()
        trajectory = mnb.from_nmea_cust_traj(nmea_cus_traj)
        self.queue.put(trajectory)


class ShipStateSubscriber(Subscriber):
    '''
    Client class for subscribing to ship states from an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def on_connect(self, client, userdata, flags, rc):
        topic = "ship_state/topic"
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            client.subscribe(topic)
            print(f"Subscribed to topic '{topic}'")

    def on_message(self, client, userdata, msg):
        # Convert NMEA string to ShipState object
        nmea_ship_state = msg.payload.decode()
        ship_state = mnb.from_nmea_cust_ship_state(nmea_ship_state)
        self.queue.put(ship_state)


class WindStateSubscriber(Subscriber):
    '''
    Client class for subscribing to wind states from an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def on_connect(self, client, userdata, flags, rc):
        topic = "wind_state/topic"
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            client.subscribe(topic)
            print(f"Subscribed to topic '{topic}'")
            
    def on_message(self, client, userdata, msg):
        # Convert NMEA string to WindState object
        nmea_wind_state = msg.payload.decode()
        wind_state = mnb.from_nmea_cust_wind_state(nmea_wind_state)
        self.queue.put(wind_state)
