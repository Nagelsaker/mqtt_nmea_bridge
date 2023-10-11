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

# TODO: These functions are placeholders.

def to_cust_traj(trajectory):
    # Convert a Python list of dictionaries representing a trajectory to a custom NMEA string
    waypoints = []
    for wp in trajectory:
        wp_str = f"{wp['lat']},{wp['lon']},{wp['heading']},{wp['actuator']},{wp['time']}"
        waypoints.append(wp_str)
    nmea_message = f"$CUSTRAJ,{';'.join(waypoints)}*checksum"
    return nmea_message

def from_cust_traj(nmea_message):
    # Convert a custom NMEA string to a Python list of dictionaries representing a trajectory
    parts = nmea_message.split(',')
    if parts[0] != "$CUSTRAJ":
        return None  # Invalid message type
    waypoints = parts[1].split(';')
    trajectory = []
    for wp_str in waypoints:
        lat, lon, heading, actuator, time = wp_str.split(',')
        wp = {'lat': lat, 'lon': lon, 'heading': heading, 'actuator': actuator, 'time': time}
        trajectory.append(wp)
    return trajectory

def to_cust_ship_state(ship_state):
    pass