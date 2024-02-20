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

    # Remove the unused data points
    if interval > dataset_interval:
        n = int(interval / dataset_interval)
        dataset = [dataset[i] for i in range(0, len(dataset), n)]
    else:
        interval = dataset_interval
    
    
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


def load_dataset(path, optimize=True, percentage=0.1):
    '''
    Loads a dataset from a CSV file.

    Columns:
    - timestamp: Time in seconds since the start of the trajectory
    - X: Ship state vector
    - CS: Course over ground and speed over ground
    - U: Actuator values vector given in percentages of maximum actuator value

    --------------------------------------------------------------------
    In:
        path (str): Path to the CSV file.
    Out:
        dataset (lst of lsts of floats): The dataset.
    --------------------------------------------------------------------
    '''
    dataset = []
    # Read the first line
    with open(path, "r") as f:
        line = f.readline()
        line = line.strip()
        line = line.split(",")
        # Read the rest of the lines
        for line in f:
            line = line.strip()
            line = line.split(",")
            time = float(line[0])
            X = [float(x.replace("\"", "").replace("[", "").replace("]", "")) for x in line[1:7]]
            COG = float(line[7].replace("\"", "").replace("[", "").replace("]", ""))
            SOG = float(line[8].replace("\"", "").replace("[", "").replace("]", ""))
            CS = [COG, SOG]
            U = [float(u.replace("\"", "").replace("[", "").replace("]", "")) for u in line[9:]]
            dataline = [time, X, CS, U]
            dataset.append(dataline)
    return dataset

def optimize_dataset_horizon(dataset, percentage):
    '''
    Will remove datapoints from the dataset if the actuator values have not changed by 'percentage' since the last datapoint.

    --------------------------------------------------------------------
    In:
        dataset (lst of lsts of floats): The dataset.
        percentage (float): The percentage change required to keep a datapoint.
    Out:
        dataset (lst of lsts of floats): The optimized dataset.
    '''
    optimized_dataset = []
    prev_U = dataset[0][3]
    optimized_dataset.append(dataset[0])
    for data_point in dataset[1:]:
        U = data_point[3]
        if not has_changed(prev_U, U, percentage):
            continue
        else:
            optimized_dataset.append(data_point)
            prev_U = U
    print(f"Optimized dataset from {len(dataset)} to {len(optimized_dataset)} datapoints.")
    return optimized_dataset

def has_changed(prev_U, U, percentage):
    '''
    Returns True if the actuator values have changed by 'percentage' since the last datapoint.

    --------------------------------------------------------------------
    In:
        prev_U (lst of floats): The actuator values from the previous datapoint.
        U (lst of floats): The actuator values from the current datapoint.
        percentage (float): The percentage change required to keep a datapoint.
    Out:
        (bool): True if the actuator values have changed by 'percentage' since the last datapoint.
    '''
    for i in range(len(U)):
        # if abs(U[i] - prev_U[i]) > (percentage/100)*prev_U[i]:
        if abs(U[i] - prev_U[i]) > (percentage/100):
            return True
    return False

if __name__ == "__main__":
    interval = int(0.5)
    remove_uneventful_points = True
    percnt_U_change = 0.1
    trajectory_from_dset_publisher(interval, remove_uneventful_points, percnt_U_change)