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
from queue import Queue
from . import from_nmea_cust_traj, from_nmea_cust_ship_state, from_nmea_cust_wind_state


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

    def connect(self):
        self.client.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def on_message(self, client, userdata, msg):
        print(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")


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
    def __init__(self, client_id, broker, port):
        super().__init__(client_id, broker, port)
        self.trajectory_queue = Queue()

    def on_message(self, client, userdata, msg):
        # Convert NMEA string to Trajectory object
        nmea_cus_traj = msg.payload.decode()
        trajectory = from_nmea_cust_traj(nmea_cus_traj)
        self.trajectory_queue.put(trajectory)


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
    def __init__(self, client_id, broker, port):
        super().__init__(client_id, broker, port)
        self.ship_state_queue = Queue()

    def on_message(self, client, userdata, msg):
        # Convert NMEA string to ShipState object
        nmea_ship_state = msg.payload.decode()
        ship_state = from_nmea_cust_ship_state(nmea_ship_state)
        self.ship_state_queue.put(ship_state)


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
    def __init__(self, client_id, broker, port):
        super().__init__(client_id, broker, port)
        self.wind_state_queue = Queue()
    
    def on_message(self, client, userdata, msg):
        # Convert NMEA string to WindState object
        nmea_wind_state = msg.payload.decode()
        wind_state = from_nmea_cust_wind_state(nmea_wind_state)
        self.wind_state_queue.put(wind_state)
