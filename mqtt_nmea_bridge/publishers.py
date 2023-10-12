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


class Publisher:
    '''
    Publisher client parent class for publishing messages to an MQTT broker.

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
        self.broker = broker
        self.port = port

    def connect(self, username, password):
        self.client.username_pw_set(f"{username}", f"{password}")
        self.client.connect(self.broker, self.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully.")
        else:
            print(f"Connect failed with return code {rc}")

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)


class TrajectoryPublisher(Publisher):
    '''
    Client class for publishing trajectories to an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def publish(self, trajectory):
        # Check if trajectory is a Trajectory object
        if not isinstance(trajectory, mnb.Trajectory):
            raise TypeError("trajectory must be a Trajectory object.")
        # Convert trajectory to custom NMEA string
        nmea_cus_traj = mnb.to_nmea_cust_traj(trajectory)
        self.client.publish("trajectory/topic", nmea_cus_traj)


class ShipStatePublisher(Publisher):
    '''
    Client class for publishing ship states to an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def publish(self, ship_state):
        # Check if ship_state is a ShipState object
        if not isinstance(ship_state, mnb.ShipState):
            raise TypeError("ship_state must be a ShipState object.")
        # Convert ship_state to custom NMEA string
        nmea_ship_state = mnb.to_nmea_cust_ship_state(ship_state)
        self.client.publish("ship_state/topic", nmea_ship_state)


class WindStatePublisher(Publisher):
    '''
    Client class for publishing wind states to an MQTT broker.

    --------------------------------------------------------------------
    Parameters:
        client_id (str): The client ID to use when connecting to the broker.
        broker (str): The IP address of the MQTT broker.
        port (int): The port number of the MQTT broker.
    --------------------------------------------------------------------
    '''
    def publish(self, wind_state):
        # Check if wind_state is a WindState object
        if not isinstance(wind_state, mnb.WindState):
            raise TypeError("wind_state must be a WindState object.")
        # Convert wind_state to custom NMEA string
        nmea_wind_state = mnb.to_nmea_cust_wind_state(wind_state)
        self.client.publish("wind_state/topic", nmea_wind_state)