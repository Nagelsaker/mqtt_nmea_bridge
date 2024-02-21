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

from utils import *
import mqtt_nmea_bridge as mnb
import time

def trajectory_from_dset_publisher(interval, remove_uneventful_points, percnt_U_change, data_path = "example_data/example_docking_trajectory.csv"):
    '''
    Loads a dataset and publishes the trajectory from the dataset to an MQTT broker.

    The data is only intended for demonstration purposes.

    The dataset is a CSV file located in 'example_data/example_docking_trajectory.csv', and contains the following columns:
    - timestamp: Time in seconds since the start of the trajectory
    - X: Ship state vector
    - U: Actuator values vector given in percentages of maximum actuator value

    X = [latitude, longitude, heading, surge_velocity, sway_velocity, yaw_rate]
    CS = [Course over ground, Speed over ground]
    U = [main_propeller_speed, main_propeller_pitch, rudder_angle, stern_thruster_speed, stern_thruster_pitch, bow_thruster_speed, bow_thruster_pitch]

    --------------------------------------------------------------------
    In:
        interval (float): The interval (in seconds) between waypoints in the trajectory.
        data_path (str): The path to the dataset.
    --------------------------------------------------------------------
    '''
    # Create a trajectory publisher that publishes a trajectory
    client_id = "trajectory_pub"
    ip = "localhost"
    port = 1883
    trajectory_pub = mnb.TrajectoryPublisher(client_id, ip, port)

    # Load the dataset
    dataset = load_dataset(data_path, remove_uneventful_points, percnt_U_change)

    # Find the time interval between each waypoint
    dataset_interval = dataset[1][0] - dataset[0][0] # The time interval between each waypoint in the dataset

    # If the interval is larger than the dataset interval, downsample the dataset
    if interval > dataset_interval:
        n = int(interval / dataset_interval)
        dataset = [dataset[i] for i in range(0, len(dataset), n)]
    else:
        interval = dataset_interval
    
    # Remove the 'uneventful' data points
    if remove_uneventful_points:
        dataset = optimize_dataset_horizon(dataset, percnt_U_change)

    print("Publishing trajectory from dataset...")
    trajectory_pub.connect(client_id, "password")
    trajectory_pub.loop_start()

    # Create a list of ShipState objects
    shipstates = []
    for data_point in dataset:
        shipstate = mnb.ShipState(time=data_point[0],
                                  latitude=data_point[1][0],
                                  longitude=data_point[1][1],
                                  heading=data_point[1][2],
                                  cog=data_point[2][0],
                                  sog=data_point[2][1],
                                  nr_of_actuators=7,
                                  actuator_values=data_point[3])
        shipstates.append(shipstate)
    
    # Publish the trajectory to the broker for 100 seconds
    trajectory = mnb.Trajectory(shipstates)
    t = 0
    start_time = time.time()
    while t < start_time + 100:
        trajectory_pub.publish(trajectory)
        time.sleep(1)
        t = time.time()

    trajectory_pub.loop_stop()



if __name__ == "__main__":
    interval = int(0.5)
    remove_uneventful_points = True
    percnt_U_change = 0.1
    trajectory_from_dset_publisher(interval, remove_uneventful_points, percnt_U_change)