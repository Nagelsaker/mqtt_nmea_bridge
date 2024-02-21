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


def wind_state_publisher_ex():
    # Create a wind state publisher that publishes a wind state
    client_id = "wind_state_pub"
    ip = "localhost"
    port = 1883
    wind_state_pub = mnb.WindStatePublisher(client_id, ip, port)

    # Timestamp in UTC seconds since 1970-01-01 00:00:00
    timestamp = 1633027200

    # Wind speed in m/s
    wind_speed = 1.0

    # Wind direction in degrees
    wind_direction = -125

    # Create the WindState object
    example_wind_state = mnb.WindState(
        time=timestamp,
        speed=wind_speed,
        direction=wind_direction
    )

    wind_state_pub.connect(client_id, "password")
    wind_state_pub.loop_start()
    t = 120
    while t > 0:
        time.sleep(1)
        wind_state_pub.publish(example_wind_state)
        t -= 1

def main():
    wind_state_publisher_ex()

if __name__ == "__main__":
    main()