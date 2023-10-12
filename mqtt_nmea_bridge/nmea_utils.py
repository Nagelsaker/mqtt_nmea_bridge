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

# *************************************************************************************************
# Helper functions for parsing NMEA0183 messages
# *************************************************************************************************

def _calculate_checksum(sentence):
    checksum = 0
    for char in sentence:
        checksum ^= ord(char)
    return checksum

def _parse_nmea_message(nmea_message):
    '''
    Parses an NMEA0183 message and returns the message type, body, and checksum.
    Verifies the checksum and issues a warning if it doesn't match.

    --------------------------------------------------------------------
    Input:
        nmea_message (str): The raw NMEA0183 message string.

    Output:
        tuple: message_type (str), message_body (str), checksum (str)
    --------------------------------------------------------------------
    '''
    # Split the message into its components
    try:
        msg_start, msg_end = nmea_message.split('*')
        message_type, message_body = msg_start[1:].split(',', 1)
    except ValueError:
        warnings.warn(f"Invalid NMEA0183 message format for the message:\n'{nmea_message}'")
        return None, None, None

    # Extract the checksum from the message
    checksum = msg_end

    # Calculate the checksum of the message content
    calculated_checksum = format(_calculate_checksum(msg_start[1:]), 'X').zfill(2)

    # Verify the checksum
    if calculated_checksum != checksum:
        warnings.warn(f"Checksum mismatch: calculated {calculated_checksum}, received {checksum}")

    return message_type, message_body, checksum

# \************************************************************************************************

# *************************************************************************************************
# * Functions to convert custom NMEA0183 messages to data objects
# *************************************************************************************************

def from_nmea_cust_traj(nmea_message):
    '''
    Converts the custom NMEA0183 message $CUSTRAJ to a Trajectory object.

    Expected NMEA message format:
    $CUSTRAJ,WP1_TIME,WP1_LAT,WP1_LON,WP1_HEADING,WP1_ACTUATOR1,WP1_ACTUATOR2,...;WP2_TIME,WP2_LAT,WP2_LON,WP2_HEADING,WP2_ACTUATOR1,WP2_ACTUATOR2,...;...*checksum

    --------------------------------------------------------------------
    Input:
        nmea_message (str): The raw NMEA0183 message string.
    Output:
        trajectory (Trajectory): The Trajectory object.
    --------------------------------------------------------------------
    '''
    msg_type, msg_body, checksum = _parse_nmea_message(nmea_message)
    if msg_type != 'CUSTRAJ':
        warnings.warn(f"Expected message type 'CUSTRAJ', got '{msg_type}'")
        return None
    waypoints = msg_body.split(';')
    timestamps = []
    latitudes = []
    longitudes = []
    headings = []
    actuator_values = []
    nr_of_actuators = None
    for waypoint in waypoints:
        timestamp, latitude, longitude, heading, *actuator_value = waypoint.split(',')
        timestamps.append(float(timestamp))
        latitudes.append(float(latitude))
        longitudes.append(float(longitude))
        headings.append(float(heading))
        actuator_value = [float(av) for av in actuator_value]
        
        if len(actuator_value) == 1:
            if nr_of_actuators is None or nr_of_actuators == 1:
                nr_of_actuators = 1
                actuator_values.append(float(actuator_value[0]))
            else:
                warnings.warn(f"Expected {nr_of_actuators} actuator values, got 1.")
                return None
        else:
            if nr_of_actuators is None or nr_of_actuators == len(actuator_value):
                nr_of_actuators = len(actuator_value)
                actuator_values.append(actuator_value)
            else:
                warnings.warn(f"Expected {nr_of_actuators} actuator values, got {len(actuator_value)}.")
                return None
            
    trajectory = mnb.Trajectory(
        timestamps=timestamps,
        latitudes=latitudes,
        longitudes=longitudes,
        headings=headings,
        actuator_values=actuator_values,
        nr_of_actuators=nr_of_actuators
    )
    return trajectory


def from_nmea_cust_ship_state(nmea_message):
    '''
    Conerts the custom NMEA0183 message $CUSSTATE to a ShipState object.

    Expected NMEA message format:
    $CUSSTATE,TIME,POS_LAT,POS_LON,POS_HEADING,POS_COG,POS_SOG,ACTUATOR1,ACTUATOR2,...*checksum

    --------------------------------------------------------------------
    Input:
        nmea_message (str): The raw NMEA0183 message string.
    Output:
        ship_state (ShipState): The ShipState object.
    --------------------------------------------------------------------
    '''
    msg_type, msg_body, checksum = _parse_nmea_message(nmea_message)
    if msg_type != 'CUSSTATE':
        warnings.warn(f"Expected message type 'CUSSTATE', got '{msg_type}'")
        return None

    # Split the message body into its components
    time, latitude, longitude, heading, cog, sog, *actuator_values = msg_body.split(',')
    actuator_values = [float(av) for av in actuator_values]
    nr_of_actuators = len(actuator_values)

    # Create a ShipState object
    ship_state = mnb.ShipState(
        time=float(time),
        latitude=float(latitude),
        longitude=float(longitude),
        heading=float(heading),
        cog=float(cog),
        sog=float(sog),
        actuator_values=actuator_values,
        nr_of_actuators=nr_of_actuators
    )
    
    return ship_state


def from_nmea_cust_wind_state(nmea_message):
    '''
    Converts the custom NMEA0183 message $CUSWIND to a WindState object.

    Expected NMEA message format:
    $CUSWIND,TIME,WIND_SPEED,WIND_DIRECTION*checksum

    --------------------------------------------------------------------
    Input:
        nmea_message (str): The raw NMEA0183 message string.
    Output:
        wind_state (WindState): The WindState object.
    --------------------------------------------------------------------
    '''
    msg_type, msg_body, checksum = _parse_nmea_message(nmea_message)
    if msg_type != 'CUSWIND':
        warnings.warn(f"Expected message type 'CUSWIND', got '{msg_type}'")
        return None

    # Split the message body into its components
    time, wind_speed, wind_direction = msg_body.split(',')

    # Create a WindState object
    wind_state = mnb.WindState(
        time=float(time),
        speed=float(wind_speed),
        direction=float(wind_direction)
    )
    
    return wind_state

# \************************************************************************************************

# *************************************************************************************************
# Functions to convert data objects to custom NMEA0183 messages
# *************************************************************************************************

def to_nmea_cust_traj(trajectory):
    '''
    Converts a Trajectory object to a custom NMEA0183 message.
    
    Outputted message format:
    $CUSTRAJ,WP1_TIME,WP1_LAT,WP1_LON,WP1_HEADING,WP1_ACTUATOR1,WP1_ACTUATOR2,...;WP2_TIME,WP2_LAT,WP2_LON,WP2_HEADING,WP2_ACTUATOR1,WP2_ACTUATOR2,...;...*checksum

    --------------------------------------------------------------------
    Input:
        trajectory (Trajectory): The Trajectory object.
    Output:
        nmea_msg (str): The custom, CUSTRAJ, NMEA0183 message.
    --------------------------------------------------------------------
    '''
    waypoints = []
    for i in range(trajectory._nr_of_waypoints):
        waypoint = [
            str(trajectory.timestamps[i]),
            str(trajectory.latitudes[i]),
            str(trajectory.longitudes[i]),
            str(trajectory.headings[i])
        ]
        waypoint += [
            str(av) for av in trajectory.actuator_values[i]
        ]
        waypoints.append(','.join(waypoint))
    sentence_body = ';'.join(waypoints)
    sentence = f"$CUSTRAJ,{sentence_body}"
    checksum = _calculate_checksum(sentence[1:])
    nmea_msg = f"{sentence}*{checksum:02X}"
    return nmea_msg


def to_nmea_cust_ship_state(ship_state):
    '''
    Converts a ShipState object to a custom NMEA0183 message.

    Outputted message format:
    $CUSSTATE,TIME,POS_LAT,POS_LON,POS_HEADING,POS_COG,POS_SOG,ACTUATOR1,ACTUATOR2,...*checksum

    --------------------------------------------------------------------
    Input:
        ship_state (ShipState): The ShipState object.
    Output:
        nmwa_msg (str): The custom, CUSSTATE, NMEA0183 message.
    --------------------------------------------------------------------
    '''
    actuator_values = [str(av) for av in ship_state.actuator_values]
    sentence_body = f"{ship_state.time},{ship_state.latitude},{ship_state.longitude},{ship_state.heading},{ship_state.cog},{ship_state.sog},{','.join(actuator_values)}"
    sentence = f"$CUSSTATE,{sentence_body}"
    checksum = _calculate_checksum(sentence[1:])
    nmea_msg = f"{sentence}*{checksum:02X}"
    return nmea_msg


def to_nmea_cust_wind_state(wind_state):
    '''
    Converts a WindState object to a custom NMEA0183 message.

    Outputted message format:
    $CUSWIND,TIME,WIND_SPEED,WIND_DIRECTION*checksum

    --------------------------------------------------------------------
    Input:
        wind_state (WindState): The WindState object.
    Output:
        nmwa_msg (str): The custom, CUSWIND, NMEA0183 message.
    --------------------------------------------------------------------
    '''
    sentence_body = f"{wind_state.time},{wind_state.speed},{wind_state.direction}"
    sentence = f"$CUSWIND,{sentence_body}"
    checksum = _calculate_checksum(sentence[1:])
    nmea_msg = f"{sentence}*{checksum:02X}"
    return nmea_msg

# \************************************************************************************************