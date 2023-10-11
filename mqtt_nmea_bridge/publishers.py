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
from nmea_utils import to_cust_traj, to_cust_ship_state


class TrajectoryPublisher:
    '''
    Client class for publishing trajectories to an MQTT broker.
    '''
    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.connect(self.broker, self.port)

    def publish(self, trajectory):
        # Convert trajectory to custom NMEA string
        nmea_cus_traj = to_cust_traj(trajectory)
        self.client.publish("trajectory/topic", nmea_cus_traj)

class ShipStatePublisher:
    '''
    Client class for publishing ship states to an MQTT broker.
    '''
    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.connect(self.broker, self.port)
    
    def publish(self, ship_state):
        # Convert ship_state to custom NMEA string
        nmea_ship_state = to_cust_ship_state(ship_state)
        self.client.publish("ship_state/topic", nmea_ship_state)