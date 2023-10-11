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

class TrajectoryPublisher:
    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.broker = broker
        self.port = port
        self.client.connect(self.broker, self.port)

    def publish(self, trajectory):
        # Convert trajectory to custom NMEA string
        nmea_message = self._convert_to_nmea(trajectory)
        self.client.publish("trajectory/topic", nmea_message)

    def _convert_to_nmea(self, trajectory):
        # Use utility functions to convert trajectory to NMEA string
        from .nmea_utils import to_nmea
        return to_nmea(trajectory)
