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
import matplotlib.pyplot as plt

def trajectory_from_dset_subscriber(visualize=False):
    '''
    Subscribes to a moving trajectory from an MQTT broker and prints the received trajectory continuously.
    '''
    client_id = "trajectory_sub"
    ip = "localhost"
    port = 1883
    trajectory_sub = mnb.TrajectorySubscriber(client_id, ip, port)
    trajectory_sub.connect(client_id, "password")
    trajectory_sub.loop_start()
    trajectory = 0

    if visualize:
        plt.ion()
        size = [6010, 5560]
        origin = [5680540.00, 586485.00]
        xlim_utm = [origin[0] - size[0] / 2, origin[0] + size[0] / 2]
        ylim_utm = [origin[1] - size[1] / 2, origin[1] + size[1] / 2]
        # xlim_ned = UTM_to_NED(xlim_utm, origin)
        # ylim_ned = UTM_to_NED(ylim_utm, origin)
        xlim = [-size[1] / 2, size[1] / 2]
        ylim = [-size[0] / 2, size[0] / 2]
        fig, ax = plt.subplots()
        ax.set_xlabel("Y [NED] (m)")
        ax.set_ylabel("X [NED] (m)")
        ax.set_title("Trajectory", fontsize=24, fontname='Times New Roman')
        ax.set_aspect('equal')
        # flip x axis
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        # ax.set_xlim(xlim_ned)
        # ax.set_ylim(ylim_ned)
        plt.show()

    time.sleep(1)
    while True:
        trajectory = trajectory_sub.get()
        if trajectory is not None and trajectory != 0:
            print(f"Received trajectory with {len(trajectory.shipstates)} ship states.")
            if visualize:
                latitudes = [shipstate.latitude for shipstate in trajectory.shipstates]
                longitudes = [shipstate.longitude for shipstate in trajectory.shipstates]
                utm_coordinates = [latlon_to_UTM(lat, lon) for lat, lon in zip(latitudes, longitudes)]
                ned_coordinates = UTM_to_NED(utm_coordinates, origin)
                ax.scatter([coord[1] for coord in ned_coordinates], [coord[0] for coord in ned_coordinates], color='b', s=5)
                plt.pause(0.1)

    

if __name__ == "__main__":
    visualize = True
    trajectory_from_dset_subscriber(visualize)