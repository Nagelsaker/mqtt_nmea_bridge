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


def wind_state_subscriber_ex():
    # Create a wind state subscriber that prints the received wind state
    client_id = "wind_state_sub"
    ip = "localhost"
    port = 1883
    wind_state_sub = mnb.WindStateSubscriber(client_id, ip, port)
    wind_state_sub.connect(client_id, "password")
    wind_state_sub.loop_start()
    t = 120
    while t > 0:
        time.sleep(1)
        t -= 1
        wind_state = wind_state_sub.get()
        if wind_state != 0:
            print(f"Wind state received. \
                    \nTimestamp: {wind_state.time} \
                    \nWind speed: {wind_state.speed} \
                    \nWind direction: {wind_state.direction} \
                    \n")

def main():
    wind_state_subscriber_ex()

if __name__ == "__main__":
    main()