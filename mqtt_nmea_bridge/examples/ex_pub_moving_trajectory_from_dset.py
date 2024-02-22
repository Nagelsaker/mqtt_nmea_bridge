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
import copy
import numpy as np

def moving_trajectory_from_dset(time_horizon=300, interval=10, sim_speed=10, remove_uneventful_points=True, percnt_U_change=0.1, data_path="example_data/example_docking_trajectory.csv"):
    '''
    Loads a dataset and publishes the trajectory from the dataset to an MQTT broker.
    The current position of the vessel is published every 'interval' seconds, together with a predicted future trajectory 'time_horizon' seconds ahead.

    NOTE: For each trajectory horizon that is published, the current position of the vessel is allways the first waypoint in the trajectory.

    The data is only intended for demonstration purposes.

    The dataset is a CSV file located in 'example_data/example_docking_trajectory.csv', and contains the following columns:
    - timestamp: Time in seconds since the start of the trajectory
    - X: Ship state vector
    - CS: Course and speed over ground
    - U: Actuator values vector given in percentages of maximum actuator value
    
    X = [latitude, longitude, heading, surge_velocity, sway_velocity, yaw_rate]
    CS = [Course over ground, Speed over ground]
    U = [main_propeller_speed, main_propeller_pitch, rudder_angle, stern_thruster_speed, stern_thruster_pitch, bow_thruster_speed, bow_thruster_pitch]

    --------------------------------------------------------------------
    In:
        time_horizon (float): The time horizon (in seconds) for the predicted trajectory.
        interval (float): The interval at which the current position of the vessel is published.
        sim_speed (float): The speed of the simulation. 1.0 is real-time.
        data_path (str): The path to the dataset.
    --------------------------------------------------------------------
    '''
    # Create a trajectory publisher that publishes a trajectory
    client_id = "trajectory_pub"
    ip = "localhost"
    port = 1883
    trajectory_pub = mnb.TrajectoryPublisher(client_id, ip, port)

    # Load the dataset
    # NOTE: We make a deep copy of the dataset to avoid modifying the original dataset
    dataset = load_dataset(data_path, remove_uneventful_points, percnt_U_change)

    # Find the time interval between each waypoint
    dataset_interval = dataset[1][0] - dataset[0][0] # The time interval between each waypoint in the dataset

    # If the interval is larger than the dataset interval, downsample the dataset
    if interval > dataset_interval:
        n = int(interval / dataset_interval)
        dataset = [dataset[i] for i in range(0, len(dataset), n)]
    else:
        interval = dataset_interval
    
    trajectory_dataset = copy.deepcopy(dataset)
    # Remove the 'uneventful' data points from the trajectory dataset
    if remove_uneventful_points:
        trajectory_dataset = optimize_dataset_horizon(trajectory_dataset, percnt_U_change)

    moving_trajectory = MovingTrajectory(trajectory_dataset, time_horizon, interval)
    print("Publishing moving trajectory from dataset...")
    trajectory_pub.connect(client_id, "password")
    trajectory_pub.loop_start()

    t = time.time()
    i = 1
    while len(moving_trajectory) > 0:
        current_time = time.time()
        if current_time - t >= interval / sim_speed:
            t = current_time
            trajectory = moving_trajectory.trajectory
            trajectory_pub.publish(trajectory)
            current_shipstate = dataset[i]
            moving_trajectory.update_moving_trajectory(current_shipstate)
            i += 1


class MovingTrajectory:
    _full_trajectory=[]
    _moving_trajectory = []

    def __init__(self, dataset, time_horizon, interval):
        '''
        MovingTrajectory class for creating a moving trajectory from a dataset.

        The time interval between each waypoint is not necessarily constant, and the number of waypoints
        in the trajectory will therefore depend on the time horizon and the time interval at which the current
        position of the vessel is published.

        --------------------------------------------------------------------
        In:
            dataset (lst of lsts of floats): The dataset.
            time_horizon (float): The time horizon (in seconds) for the predicted trajectory.
            interval (float): The interval at which the current position of the vessel is published.
        '''
        self._full_trajectory = dataset
        self._time_horizon = time_horizon
        self._interval = interval
        self._prev_timestamp = self._full_trajectory[0][0]
        init_shipstate = self._full_trajectory[0]
        self.update_moving_trajectory(init_shipstate)

    def update_moving_trajectory(self, current_shipstate):
        '''
        Update the moving trajectory from the dataset.
        The current position of the vessel is the first ShipState object in the trajectory.

        The time interval between each waypoint is not necessarily constant, and the number of waypoints
        in the trajectory will therefore depend on the time horizon and the time interval at which the current
        position of the vessel is published.

        --------------------------------------------------------------------
        In:
            timestamp (float): The timestamp of the current position of the vessel.
        Out:
            moving_trajectory (lst of lsts of floats): The moving trajectory.
        --------------------------------------------------------------------
        '''
        timestamp = current_shipstate[0]
        # Optimize the search range in the full trajectory
        # TODO: Implement a more efficient search algorithm

        # Find the start index from the full trajectory
        start_idx_full_traj = np.where(np.array(self._full_trajectory, dtype=object)[:,0] == timestamp)[0]
        if len(start_idx_full_traj) == 0:
            start_idx_full_traj = 0
        else:
            start_idx_full_traj = start_idx_full_traj[0]
        # Find the end index from the full trajectory
        end_time = timestamp + self._time_horizon
        end_horizon_idx = np.where(np.array(self._full_trajectory, dtype=object)[:,0] >= end_time)[0]
        if len(end_horizon_idx) == 0:
            end_horizon_idx = len(self._full_trajectory)-1
        else:
            end_horizon_idx = end_horizon_idx[0]
            # if self._full_trajectory[end_horizon_idx][0] - end_time > 10:
            #     end_horizon_idx -= 1
        
        # Find the start index from the moving trajectory
        if len(self._moving_trajectory) == 0:
            start_idx_moving_traj = -1
        else:
            start_idx_moving_traj = np.where(np.array(self._moving_trajectory, dtype=object)[:,0] >= timestamp)[0]
            if len(start_idx_moving_traj) == 0:
                start_idx_moving_traj = -1
            else:
                start_idx_moving_traj = start_idx_moving_traj[0]

        # If currrent ShipState already in moving trajectory and only waypoint left
        if start_idx_moving_traj == 0:
            self._moving_trajectory = []
        # If the start index from the moving trajectory is not found, create a new moving trajectory
        elif start_idx_moving_traj == -1: # If the current position of the vessel is not in the moving trajectory
            # if end_horizon_idx == -1: # If the entire trajectory shall be published at once (horizon exceeds dataset length)
            #     self._moving_trajectory = self._full_trajectory[start_idx_full_traj:]
            # else: # If the horizon is within the dataset length
            self._moving_trajectory = self._full_trajectory[start_idx_full_traj:end_horizon_idx+1]
        else: # If the current position of the vessel is in the moving trajectory
            self._moving_trajectory = self._moving_trajectory[start_idx_moving_traj:]
            if len(self._full_trajectory) == 0: # If the full trajectory is empty
                pass
            elif end_horizon_idx == -1: # If next timestamp in full horizon is far into the future
                pass
                # self._moving_trajectory.append(self._full_trajectory[start_idx_full_traj:])
            else: # If current position already in moving trajectory and horizon is within the dataset length
                if start_idx_full_traj == end_horizon_idx:
                    self._moving_trajectory.append(self._full_trajectory[start_idx_full_traj:end_horizon_idx+1][0])
                else:
                    self._moving_trajectory.append(self._full_trajectory[start_idx_full_traj:end_horizon_idx+1])

        # Remove the appended waypoints from the full trajectory
        if len(self._full_trajectory) > 0:
            self._full_trajectory = self._full_trajectory[end_horizon_idx+1:]
        
        # Check if the current position of the vessel is in the moving trajectory
        if len(self._moving_trajectory) > 0:
            if self._moving_trajectory[0][0] == timestamp:
                pass
            else:
                self._moving_trajectory.insert(0, current_shipstate)

        print(f"Moving trajectory length: {len(self._moving_trajectory)}\nFull trajectory length: {len(self._full_trajectory)}")

    @property
    def trajectory(self):
        shipStates = []
        for data_point in self._moving_trajectory:
            shipstate = mnb.ShipState(time=data_point[0],
                                    latitude=data_point[1][0],
                                    longitude=data_point[1][1],
                                    heading=data_point[1][2],
                                    cog=data_point[2][0],
                                    sog=data_point[2][1],
                                    nr_of_actuators=7,
                                    actuator_values=data_point[3])
            shipStates.append(shipstate)
        trajectory = mnb.Trajectory(shipStates)
        return trajectory
    
    def __len__(self):
        return len(self._moving_trajectory)
    
if __name__ == "__main__":
    time_horizon=300
    interval=10
    sim_speed=10
    remove_uneventful_points=True
    percnt_U_change=0.1
    moving_trajectory_from_dset(time_horizon, interval, sim_speed, remove_uneventful_points, percnt_U_change)