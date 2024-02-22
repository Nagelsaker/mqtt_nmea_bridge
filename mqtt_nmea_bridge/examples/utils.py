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

from pyproj import Transformer


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

def latlon_to_UTM(lat, lon):
    '''
    Converts lat/lon to UTM zone 31 coordinates

    --------------------------------------------------
    In:
        lat: (Float) Latitude
        lon: (Float) Longitude
    Out:
        northing: (Float) Northing coordinate
        easting: (Float) Easting coordinate
    '''
    # Create a transformer object for converting from WGS84 to UTM Zone 31
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32631")
    
    # Convert
    easting, northing = transformer.transform(lat, lon)
    
    return northing, easting


def UTM_to_NED(UTM, origin, is_dict=False):
    '''
    Converts UTM coordinates to NED coordinates.

    --------------------------------------------------
    In:
        UTM: (List[float, float]) Northing, Easting coordinates
        or
        UTM: (List[List[float, float]]) List of Northing, Easting coordinates
        origin: (List[float, float]) Northing, Easting coordinates of origin
    Out:
        NED: (List[float, float]) North, East coordinates
        or
        NED: (List[List[float, float]]) List of North, East coordinates
    '''
    if is_dict:
        NED = {}
        for key, value in UTM.items():
            NED[key] = UTM_to_NED(value, origin)
        return NED
    else:
        if UTM == [] or isinstance(UTM, int) or isinstance(UTM, float):
            return UTM
        if isinstance(UTM[0], list) or isinstance(UTM[0], tuple):
            if isinstance(UTM[0][0], list) or isinstance(UTM[0][0], tuple):
                NED = [[[point[0]-origin[0], point[1]-origin[1]] for point in poly] for poly in UTM]
            else:
                NED = [[point[0]-origin[0], point[1]-origin[1]] for point in UTM]
        else:
            NED = [UTM[0]-origin[0], UTM[1]-origin[1]]
        return NED