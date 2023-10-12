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
$CUSSTATE,TIME,POS_LAT,POS_LON,POS_HEADING,POS_COG,POS_SOG,ACTUATOR1,ACTUATOR2,...*checksum
```

**TIME** is the time in UTC seconds since 1970-01-01 00:00:00. **POS_LAT** and **POS_LON** are the latitude and longitude of the vessel. **POS_HEADING** is the heading of the vessel in radians. **POS_COG** is the course over ground of the vessel in radians. **POS_SOG** is the speed over ground of the vessel in m/s. **WP1_ACTUATOR1**, **WP1_ACTUATOR2**, ... are the actuator values at the given time.

### Wind state
```
$CUSWIND,TIME,WIND_SPEED,WIND_DIRECTION*checksum
```

**TIME** is the time in UTC seconds since 1970-01-01 00:00:00. **WIND_SPEED** is the wind speed in m/s. **WIND_DIRECTION** is the wind direction in radians.

All angular directions are in radians with 0 being north, pi/2 being east, pi/-pi being south, and -pi/2 being west.

## Usage
The module can be run in a Python script. Please look at the example files in the examples folder for more information.
The examples work with the local Eclipse Mosquitto broker. 

To install the broker on Ubuntu v22.04, run:
```shell
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
sudo apt clean
```

Setup the WebUI Manager by running:
```shell
docker run -it -v ~/cedalo_platform:/cedalo cedalo/installer:2-linux
```
Select the preconfigured option and install.

The broker can now be started by running:
```shell
cd ~/cedalo_platform
sh start.sh
```

The WebUI Manager can be accessed at http://localhost:8080
With the default credentials, username: cedalo, password: mmcisawesome

Make sure to setup clients for the publishers and subscribers. This can be done by clicking on the "Clients" tab in the WebUI Manager. With the credentials used in the examples properly set up, the WebUI Manager should look like this:

![Alt text](figures/WebUI_credentials.png)