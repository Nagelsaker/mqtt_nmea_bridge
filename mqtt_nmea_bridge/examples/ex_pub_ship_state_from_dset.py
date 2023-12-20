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


def ship_state_from_dset_publisher_ex(interval=0.5, simulation_speed=10, data_path = "example_data/example_docking_trajectory.csv"):
    '''
    Loads a dataset and publishes the ship state from the dataset to an MQTT broker.

    Note, the data is should be taken with a grain of salt, and does not represent
    an energy-efficient and safe docking trajectory. The data is only used for demonstration purposes.

    The dataset is a CSV file located in 'example_data/example_docking_trajectory.csv', and contains the following columns:
    - timestamp: Time in seconds since the start of the trajectory
    - X: Ship state vector
    - U: Actuator values vector given in percentages of maximum actuator value

    X = [latitude, longitude, heading, surge_velocity, sway_velocity, yaw_rate]
    U = [main_propeller_speed, main_propeller_pitch, rudder_angle, stern_thruster_speed, stern_thruster_pitch, bow_thruster_speed, bow_thruster_pitch]

    The interval between each data point is 0.5 seconds, and the trajectory is over 41 minutes long.
    Increase the interval to reduce the number of published messages.
    Increase the simulation_speed to increase the rate at which the ship state is published.

    --------------------------------------------------------------------
    In:
        interval (float): The interval between each published ship state.
        simulation_speed (int): 1 = real-time, 2 = 2x real-time, etc.
    --------------------------------------------------------------------
    '''
    # Create a ship state publisher that publishes a ship state
    client_id = "ship_state_pub"
    ip = "localhost"
    port = 1883
    ship_state_pub = mnb.ShipStatePublisher(client_id, ip, port)

    # Load the dataset
    dataset = load_dataset(data_path)


def load_dataset(path):
    '''
    Loads a dataset from a CSV file.

    Columns:
    - timestamp: Time in seconds since the start of the trajectory
    - X: Ship state vector
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
            dataset.append(line)
    return dataset


def main():
    interval = 0.5
    simulation_speed = 10
    ship_state_from_dset_publisher_ex(interval=interval, simulation_speed=simulation_speed)

if __name__ == "__main__":
    main()