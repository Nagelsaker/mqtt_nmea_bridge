# mqtt_nmea_bridge
MQTT-NMEA-BRIDGE serves as a data link layer, translating and routing messages via MQTT while adhering to custom NMEA0183 message formats. The module aims to synchronize real-time vessel data and control commands for autonomous docking operations


## Installation

Clone this repository to any folder. From the same folder, run:
```
pip install -e .
```

## Custom NMEA0183 messages
The messages are on the format:

### Trajectory
```
$CUSTRAJ,WP1_TIME,WP1_LAT,WP1_LON,WP1_HEADING,WP1_ACTUATOR1,WP1_ACTUATOR2,...;WP2_TIME,WP2_LAT,WP2_LON,WP2_HEADING,WP2_ACTUATOR1,WP2_ACTUATOR2,...;...*checksum
```

**WP1_TIME** is the time in UTC seconds since 1970-01-01 00:00:00 at the first waypoint. **WP1_LAT** and **WP1_LON** are the latitude and longitude at the first waypoint. **WP1_HEADING** is the heading of the vessel in radians at the first waypoint. **WP1_ACTUATOR1**, **WP1_ACTUATOR2**, ... are the actuator values at the first waypoint. The same parameters are used for the second waypoint, and so on.

### Ship state
```
$CUSSTATE,TIME,POS_LAT,POS_LON,POS_HEADING,POS_COG,POS_SOG*checksum
```

**TIME** is the time in UTC seconds since 1970-01-01 00:00:00. **POS_LAT** and **POS_LON** are the latitude and longitude of the vessel. **POS_HEADING** is the heading of the vessel in radians. **POS_COG** is the course over ground of the vessel in radians. **POS_SOG** is the speed over ground of the vessel in m/s.

### Wind state
```
$CUSWIND,TIME,WIND_SPEED,WIND_DIRECTION*checksum
```

**TIME** is the time in UTC seconds since 1970-01-01 00:00:00. **WIND_SPEED** is the wind speed in m/s. **WIND_DIRECTION** is the wind direction in radians.

All angular directions are in radians with 0 being north, pi/2 being east, pi/-pi being south, and -pi/2 being west.

## Usage
The module can be run in a Python script.

### Publishing messages
The following example shows how to publish a trajectory message to the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb

# Create a trajectory message
# TODO: Add example
```

The following example shows how to publish a ship state message to the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb
# TODO: Add example
```

The following example shows how to publish a wind state message to the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb
# TODO: Add example
```

### Subscribing to messages
The following example shows how to subscribe to a trajectory message from the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb
# TODO: Add example
```

The following example shows how to subscribe to a ship state message from the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb
# TODO: Add example
```

The following example shows how to subscribe to a wind state message from the MQTT broker at localhost.
```python
import mqtt_nmea_bridge as mnb
# TODO: Add example
```