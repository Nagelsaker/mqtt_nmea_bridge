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


def trajectory_subscriber_ex():
    # Create a trajectory subscriber that prints the received trajectory
    client_id = "traj_sub"
    ip = "localhost"
    port = 1883
    traj_sub = mnb.TrajectorySubscriber(client_id, ip, port)
    traj_sub.connect(client_id, "password")
    traj_sub.loop_start()
    t = 120
    while t > 0:
        time.sleep(1)
        t -= 1
        trajectory = traj_sub.get()
        if trajectory != 0:
            print(f"Trajectory received. \
                    \nTimestamps: {trajectory.timestamps} \
                    \nLatitudes: {trajectory.latitudes} \
                    \nLongitudes: {trajectory.longitudes} \
                    \nHeadings: {trajectory.headings} \
                    \nActuator values: {trajectory.actuator_values} \
                    \nNumber of actuators: {trajectory.nr_of_actuators} \
                    \n")

def main():
    trajectory_subscriber_ex()

if __name__ == "__main__":
    main()