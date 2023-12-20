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
import mqtt_nmea_bridge as mnb
import warnings
import json

# *************************************************************************************************
# Helper functions for parsing NMEA0183 messages
# *************************************************************************************************

def _calculate_checksum(sentence):
    '''
    Warning! Deprecated.
    '''
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return checksum

def _parse_mqtt_str(mqtt_str):
    '''
    Parses an mqtt JSON string and returns the message type and body

    --------------------------------------------------------------------
    Input:
        mqtt_str (str): The JSON formatted string.

    Output:
        tuple: message_type (str), message_body (dict)
    --------------------------------------------------------------------
    '''
    # Split the message into its components
    mqtt_dict = json.loads(mqtt_str)
    message_type = mqtt_dict["type"]
    message_body = mqtt_dict["body"]

    return message_type, message_body

# \************************************************************************************************

# *************************************************************************************************
# * Functions to convert custom NMEA0183 messages to data objects
# *************************************************************************************************

def from_mqtt_str_to_traj(mqtt_str):
    '''
    Converts the mqtt JSON string to a Trajectory object.

    --------------------------------------------------------------------
    Input:
        mqtt_str (str): The JSON formatted string.
    Output:
        trajectory (Trajectory): The Trajectory object.
    --------------------------------------------------------------------
    '''
    # Parse the mqtt string
    msg_type, msg_body = _parse_mqtt_str(mqtt_str)

    # Check if the message type is 'TRAJ'
    if msg_type != 'TRAJ':
        warnings.warn(f"Expected message type 'TRAJ', got '{msg_type}'")
        return None
    
    # Check if the message body contains the correct keys
    if not all(key in msg_body for key in ["type", "body"]):
        warnings.warn(f"Expected message body to contain keys 'type' and 'body'.")
        return None
    
    # Check if the message body contains the correct keys
    if not all(key in msg_body["body"] for key in ["type", "body"]):
        warnings.warn(f"Expected message body to contain keys 'type' and 'body'.")
        return None
    
    # Check if the message body contains the correct keys
    if not all(key in msg_body["body"]["body"] for key in ["time", "latitude", "longitude", "heading", "cog", "sog", "nr_of_actuators", "actuator_values"]):
        warnings.warn(f"Expected message body to contain keys 'time', 'latitude', 'longitude', 'heading', 'cog', 'sog', 'nr_of_actuators', and 'actuator_values'.")
        return None
    
    # Create a Trajectory object from the message body
    trajectory = mnb.Trajectory(
        shipstates=[
            mnb.ShipState(
                time=ship_state["time"],
                latitude=ship_state["latitude"],
                longitude=ship_state["longitude"],
                heading=ship_state["heading"],
                cog=ship_state["cog"],
                sog=ship_state["sog"],
                nr_of_actuators=ship_state["nr_of_actuators"],
                actuator_values=ship_state["actuator_values"]
            )
            for ship_state in msg_body["body"]["body"]
        ]
    )

    return trajectory


def from_mqtt_str_to_shipstate(mqtt_str):
    '''
    Conerts the custom mqtt JSON string to a ShipState object.


    --------------------------------------------------------------------
    Input:
        mqtt_str (str): The JSON formatted string.
    Output:
        ship_state (ShipState): The ShipState object.
    --------------------------------------------------------------------
    '''
    # Parse the mqtt string
    msg_type, msg_body = _parse_mqtt_str(mqtt_str)

    # Check if the message type is 'SHIP_STATE'
    if msg_type != 'SHIP_STATE':
        warnings.warn(f"Expected message type 'SHIP_STATE', got '{msg_type}'")
        return None
    
    # Check if the message body contains the correct keys
    if not all(key in msg_body for key in ["time", "latitude", "longitude", "heading", "cog", "sog", "nr_of_actuators", "actuator_values"]):
        warnings.warn(f"Expected message body to contain keys 'time', 'latitude', 'longitude', 'heading', 'cog', 'sog', 'nr_of_actuators', and 'actuator_values'.")
        return None
    
    # Create a ShipState object from the message body
    ship_state = mnb.ShipState(
        time=msg_body["time"],
        latitude=msg_body["latitude"],
        longitude=msg_body["longitude"],
        heading=msg_body["heading"],
        cog=msg_body["cog"],
        sog=msg_body["sog"],
        nr_of_actuators=msg_body["nr_of_actuators"],
        actuator_values=msg_body["actuator_values"]
    )

    return ship_state



def from_mqtt_str_to_windstate(mqtt_str):
    '''
    Converts the custom mqtt JSON string to a WindState object.

    --------------------------------------------------------------------
    Input:
        mqtt_str (str): The JSON formatted string.
    Output:
        wind_state (WindState): The WindState object.
    --------------------------------------------------------------------
    '''
    # Parse the mqtt string
    msg_type, msg_body = _parse_mqtt_str(mqtt_str)

    # Check if the message type is 'WIND_STATE'
    if msg_type != 'WIND_STATE':
        warnings.warn(f"Expected message type 'WIND_STATE', got '{msg_type}'")
        return None
    
    # Check if the message body contains the correct keys
    if not all(key in msg_body for key in ["time", "speed", "direction"]):
        warnings.warn(f"Expected message body to contain keys 'time', 'speed', and 'direction'.")
        return None
    
    # Create a WindState object from the message body
    wind_state = mnb.WindState(
        time=msg_body["time"],
        speed=msg_body["speed"],
        direction=msg_body["direction"]
    )

    return wind_state

# \************************************************************************************************

# *************************************************************************************************
# Functions to convert data objects to custom NMEA0183 messages
# *************************************************************************************************

def from_traj_to_mqtt_str(trajectory):
    '''
    Converts a Trajectory object to a JSON string.

    Outputted message on the JSON format:
    {
        "type": "TRAJ",
        "body": [
            {
                "type": "SHIP_STATE",
                "body":
                    {
                        "time": WP1_TIME,
                        "latitude": WP1_LAT,
                        "longitude": WP1_LON,
                        "heading": WP1_HEADING,
                        "cog": WP1_COG, # 'None' if not available
                        "sog": WP1_SOG,
                        "nr_of_actuators": WP1_NR_OF_ACTUATORS, # Constant for all waypoints
                        "actuator_values": [WP1_ACTUATOR1, WP1_ACTUATOR2, ...]
                    }
            },
            {
                "type": "SHIP_STATE",
                "body":
                    {
                        "time": WP2_TIME,
                        "latitude": WP2_LAT,
                        "longitude": WP2_LON,
                        "heading": WP2_HEADING,
                        "cog": WP1_COG,
                        "sog": WP2_SOG,
                        "nr_of_actuators": WP2_NR_OF_ACTUATORS,
                        "actuator_values": [WP2_ACTUATOR1, WP2_ACTUATOR2, ...]
                    }
            },
            ...
        ]
    }

    --------------------------------------------------------------------
    Input:
        trajectory (Trajectory): The Trajectory object.
    Output:
        mqtt_str (str): JSON formatted string of trajectory object.
    --------------------------------------------------------------------
    '''
    # Check if trajectory is a Trajectory object
    if not isinstance(trajectory, mnb.Trajectory):
        raise TypeError("trajectory must be a Trajectory object.")
    
    # Create a dictionary from the Trajectory object
    trajectory_dict = {
        "type": "TRAJ",
        "body": []
    }
    for ship_state in trajectory.shipstates:
        ship_state_dict = {
            "type": "SHIP_STATE",
            "body": {
                "time": ship_state.time,
                "latitude": ship_state.latitude,
                "longitude": ship_state.longitude,
                "heading": ship_state.heading,
                "cog": ship_state.cog,
                "sog": ship_state.sog,
                "nr_of_actuators": ship_state.nr_of_actuators,
                "actuator_values": ship_state.actuator_values
            }
        }
        trajectory_dict["body"].append(ship_state_dict)

    # Convert the dictionary to a JSON string
    trajectory_str = json.dumps(trajectory_dict)
    return trajectory_str


def from_shipstate_to_mqtt_str(ship_state):
    '''
    Converts a ShipState object to a JSON string

    Outputted message on the JSON format:
    {
        "type": "SHIP_STATE",
        "body": {
            "time": TIME,
            "latitude": LAT,
            "longitude": LON,
            "heading": HEADING,
            "cog": COG, # 'None' if not available
            "sog": SOG,
            "nr_of_actuators": NR_OF_ACTUATORS,
            "actuator_values": [ACTUATOR1, ACTUATOR2, ...]
        }
    }

    --------------------------------------------------------------------
    Input:
        ship_state (ShipState): The ShipState object.
    Output:
        mqtt_str (str): JSON formatted string of ship_state object.
    --------------------------------------------------------------------
    '''
    # Check if ship_state is a ShipState object
    if not isinstance(ship_state, mnb.ShipState):
        raise TypeError("ship_state must be a ShipState object.")
    
    # Create a dictionary from the ShipState object
    ship_state_dict = {
        "type": "SHIP_STATE",
        "body": {
            "time": ship_state.time,
            "latitude": ship_state.latitude,
            "longitude": ship_state.longitude,
            "heading": ship_state.heading,
            "cog": ship_state.cog,
            "sog": ship_state.sog,
            "nr_of_actuators": ship_state.nr_of_actuators,
            "actuator_values": ship_state.actuator_values
        }
    }

    # Convert the dictionary to a JSON string
    ship_state_str = json.dumps(ship_state_dict)
    return ship_state_str


def from_windstate_to_mqtt_str(wind_state):
    '''
    Converts a WindState object to a JSON string

    Outputted message on the JSON format:
    {
        "type": "WIND_STATE",
        "body": {
            "time": TIME,
            "speed": SPEED,
            "direction": DIRECTION
        }
    }

    --------------------------------------------------------------------
    Input:
        wind_state (WindState): The WindState object.
    Output:
        nmwa_msg (str): JSON formatted string of wind_state object.
    --------------------------------------------------------------------
    '''
    # Check if wind_state is a WindState object
    if not isinstance(wind_state, mnb.WindState):
        raise TypeError("wind_state must be a WindState object.")
    
    # Create a dictionary from the WindState object
    wind_state_dict = {
        "type": "WIND_STATE",
        "body": {
            "time": wind_state.time,
            "speed": wind_state.speed,
            "direction": wind_state.direction
        }
    }

    # Convert the dictionary to a JSON string
    wind_state_str = json.dumps(wind_state_dict)

    return wind_state_str

# \************************************************************************************************