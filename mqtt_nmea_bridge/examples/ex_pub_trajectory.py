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


def trajectory_publisher_ex():
    # Create a trajectory publisher that publishes a trajectory
    client_id = "traj_pub"
    ip = "localhost"
    port = 1883
    traj_pub = mnb.TrajectoryPublisher(client_id, ip, port)

    # Timestamps in UTC seconds since 1970-01-01 00:00:00
    timestamps = [1633027200, 1633027260, 1633027320, 1633027380]

    # Latitudes in decimal degrees
    latitudes = [63.446827, 63.446924, 63.447021, 63.447118]

    # Longitudes in decimal degrees
    longitudes = [10.421905, 10.421806, 10.421707, 10.421608]

    # Headings in radians
    headings = [0.7854, 0.7854, 0.7854, 0.7854]

    # Actuator values (could be throttle, rudder angle, etc.)
    # Here, assuming 2 actuators for simplicity
    actuator_values = [
        [0.5, 0.2],
        [0.6, 0.3],
        [0.7, 0.4],
        [0.8, 0.5]
    ]

    # Number of actuators
    nr_of_actuators = 2

    # Create the Trajectory object
    example_trajectory = mnb.Trajectory(
        timestamps=timestamps,
        latitudes=latitudes,
        longitudes=longitudes,
        headings=headings,
        actuator_values=actuator_values,
        nr_of_actuators=nr_of_actuators
    )

    traj_pub.connect(client_id, "password")
    traj_pub.loop_start()
    t = 120
    while t > 0:
        time.sleep(1)
        traj_pub.publish(example_trajectory)
        t -= 1

def main():
    trajectory_publisher_ex()

if __name__ == "__main__":
    main()