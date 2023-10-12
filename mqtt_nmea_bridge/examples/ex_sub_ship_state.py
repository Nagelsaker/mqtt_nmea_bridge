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


def ship_state_subscriber_ex():
    # Create a ship state subscriber that prints the received ship state
    client_id = "ship_state_sub"
    ip = "localhost"
    port = 1883
    ship_state_sub = mnb.ShipStateSubscriber(client_id, ip, port)
    ship_state_sub.connect(client_id, "password")
    ship_state_sub.loop_start()
    t = 120
    while t > 0:
        time.sleep(1)
        t -= 1
        ship_state = ship_state_sub.get()
        if ship_state != 0:
            print(f"Ship state received. \
                    \nTimestamp: {ship_state.time} \
                    \nLatitude: {ship_state.latitude} \
                    \nLongitude: {ship_state.longitude} \
                    \nHeading: {ship_state.heading} \
                    \nCOG: {ship_state.cog} \
                    \nSOG: {ship_state.sog} \
                    \nActuator values: {ship_state.actuator_values} \
                    \nNumber of actuators: {ship_state.nr_of_actuators} \
                    \n")

def main():
    ship_state_subscriber_ex()

if __name__ == "__main__":
    main()