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
$CUSTRAJ,WP1_LAT,WP1_LON,WP1_HEADING,WP1_ACTUATOR1,WP1_TIME;WP2_LAT,WP2_LON,WP2_HEADING,WP2_ACTUATOR,WP2_TIME;...\*checksum
```

### Ship state
```
$CUSSTATE,TIME,POS_LAT,POS_LON,POS_HEADING,POS_COG,POS_SOG\*checksum
```

### Wind state
```
$CUSWIND,TIME,WIND_FORCE,WIND_DIRECTION\*checksum
```