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

def trajectory_from_dset_subscriber():
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
    time.sleep(1)
    while True:
        trajectory = trajectory_sub.get()
        if trajectory is not None and trajectory != 0:
            print(f"Received trajectory with {len(trajectory.shipstates)} ship states.")
    

if __name__ == "__main__":
    trajectory_from_dset_subscriber()