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
from dataclasses import dataclass


@dataclass
class Trajectory:
    '''
    Dataclass for representing a trajectory.
    The trajectory consists of a list of latitudes, a list of longitudes, a list of actuator values, and a list of timestamps.
    All lists must be of equal length.

    --------------------------------------------------------------------
    Parameters:

    shipstates: list of ShipState objects
    --------------------------------------------------------------------
    '''
    shipstates: list

    def __post_init__(self):
        self._nr_of_waypoints: int = len(self.shipstates)

        # Check if shipstates is a list of ShipState objects
        for shipstate in self.shipstates:
            if not isinstance(shipstate, ShipState):
                raise TypeError("The shipstates list can only contain ShipState objects.")
        

@dataclass
class ShipState:
    '''
    Dataclass for representing the state of a ship.

    --------------------------------------------------------------------
    Parameters:

    time (float): In seconds
    latitude (float)
    longitude (float)
    heading (float): In radians
    cog (float): Course Over Ground in radians. Can be 'None' if not available.
    sog (float): Speed Over Ground in radians n m/s
    actuator_values (lst of floats / lst of lsts of floats): On the format [a1, a2, ...]
    nr_of_actuators (int)
    --------------------------------------------------------------------
    '''
    time: float
    latitude: float
    longitude: float
    heading: float
    cog: float
    sog: float
    nr_of_actuators: int
    actuator_values: list


@dataclass
class WindState:
    '''
    Dataclass for representing the state of the wind.

    --------------------------------------------------------------------
    Parameters:

    time: (float) In UTC seconds since 1970-01-01 00:00:00
    speed: (float) In m/s
    direction: (float) In radians from north (0) to east (pi/2) to south (pi or -pi) to west (-pi/2)
    --------------------------------------------------------------------
    '''
    time: float
    speed: float
    direction: float