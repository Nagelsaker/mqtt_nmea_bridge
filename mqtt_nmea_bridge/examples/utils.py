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