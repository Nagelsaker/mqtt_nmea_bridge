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
import time


def ship_state_publisher_ex():
    # Create a ship state publisher that publishes a ship state
    client_id = "ship_state_pub"
    ip = "localhost"
    port = 1883
    ship_state_pub = mnb.ShipStatePublisher(client_id, ip, port)

    # Timestamp in UTC seconds since 1970-01-01 00:00:00
    #  Northing=5683020.00, Easting=587730.00
    timestamp = 1633027200

    # Latitude in decimal degrees
    # latitude = 63.446827
    latitude = 51.29174

    # Longitude in decimal degrees
    # longitude = 10.421905
    longitude = 4.258185

    # Heading in radians
    heading = 0.7854

    # Course over ground in radians
    cog = 0.7854

    # Speed over ground in m/s
    sog = 1.0

    # Actuator values (could be throttle, rudder angle, etc.)
    # Here, assuming 2 actuators for simplicity
    actuator_values = [0.5, 0.2]

    # Number of actuators
    nr_of_actuators = 2

    # Create the ShipState object
    example_ship_state = mnb.ShipState(
        time=timestamp,
        latitude=latitude,
        longitude=longitude,
        heading=heading,
        cog=cog,
        sog=sog,
        actuator_values=actuator_values,
        nr_of_actuators=nr_of_actuators
    )

    ship_state_pub.connect(client_id, "password")
    ship_state_pub.loop_start()
    t = 120
    # while t > 0:
    while True:
        time.sleep(1)
        ship_state_pub.publish(example_ship_state)
        t -= 1

def main():
    ship_state_publisher_ex()

if __name__ == "__main__":
    main()