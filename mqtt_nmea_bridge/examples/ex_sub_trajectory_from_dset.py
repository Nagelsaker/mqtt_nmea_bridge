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
import mqtt_nmea_bridge as mnb
import matplotlib.pyplot as plt
import numpy as np
import time


def trajectory_subscriber_ex():
    # Create a trajectory subscriber that prints the received trajectory
    client_id = "trajectory_sub"
    ip = "localhost"
    port = 1883
    trajectory_sub = mnb.TrajectorySubscriber(client_id, ip, port)
    trajectory_sub.connect(client_id, "password")
    trajectory_sub.loop_start()
    trajectory = 0
    time.sleep(1)
    while True:
        trajectory = trajectory_sub.get()
        if trajectory is not None and trajectory != 0:
            break
    
    # Extract the latitudes and longitudes from the trajectory
    latitudes = [shipstate.latitude for shipstate in trajectory.shipstates]
    longitudes = [shipstate.longitude for shipstate in trajectory.shipstates]

    # Convert the lat/lon to UTM coordinates
    utm_coordinates = [latlon_to_UTM(lat, lon) for lat, lon in zip(latitudes, longitudes)]

    # Convert UTM to NED coordinates
    origin = [586485.00, 5680540.00]
    ned_coordinates = UTM_to_NED(utm_coordinates, origin)

    plot_type = "points"
    if plot_type != "none":
        if plot_type == "line":
            plt.plot([coord[0] for coord in utm_coordinates], [coord[1] for coord in ned_coordinates])
            plt.xlabel("Y [NED] (m)")
            plt.ylabel("X [NED] (m)")
            plt.title("Trajectory", fontsize=24, fontname='Times New Roman')
        elif plot_type == "points":
            # Plot the trajectory as individual points
            plt.scatter([coord[0] for coord in utm_coordinates], [coord[1] for coord in ned_coordinates])
            plt.xlabel("Y [NED] (m)", fontsize=18, fontname='Times New Roman')
            plt.ylabel("X [NED] (m)", fontsize=18, fontname='Times New Roman')
            plt.title("Trajectory", fontsize=24, fontname='Times New Roman')
        elif plot_type == "buckets":
            t_iv = [shipstate.time for shipstate in trajectory.shipstates]
            # Calculate the time intervals between consecutive actuator value changes
            time_intervals = np.diff(t_iv)  # numpy's diff function calculates the difference between consecutive elements in the list
            
            # Define the buckets for the histogram. You can adjust the bins according to the range and precision you find most informative
            bins = np.arange(0, max(time_intervals) + 0.5, 0.5)  # Adjust the step to match your expected resolution
            
            # Plot the histogram
            plt.hist(time_intervals, bins=bins, alpha=0.75, color='blue', edgecolor='black')
            
            # Labeling the plot
            plt.yscale('log')
            hlines = [1e+0, 1e+1, 1e+2, 1e+3]
            for hline in hlines:
                plt.axhline(y=hline, color='gray', linestyle='--', alpha=0.5)
            plt.xlabel("Time intervals between actuator changes (s)", fontsize=18, fontname='Times New Roman')
            plt.ylabel("Count (log scale)", fontsize=18, fontname='Times New Roman')
            plt.title("Distribution of Time Intervals between Actuator Value Changes", fontsize=24, fontname='Times New Roman')  # Larger font size for title
        plt.show()

    trajectory_sub.loop_stop()


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


if __name__ == "__main__":
    trajectory_subscriber_ex()