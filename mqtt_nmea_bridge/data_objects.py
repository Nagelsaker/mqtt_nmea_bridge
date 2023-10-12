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

    timestamps (lst of floats):  In UTC seconds since 1970-01-01 00:00:00
    latitudes (lst of floats)
    longitudes (lst of floats)
    headings (lst of floats): In radians
    actuator_values (lst of floats / lst of lsts of floats): On the format [[w1_a1, w1_a2, ...], [w2_a1, w2_a2, ...], ...]
    nr_of_actuators (int)
    --------------------------------------------------------------------
    '''
    timestamps: list
    latitudes: list
    longitudes: list
    headings: list
    actuator_values: list
    nr_of_actuators: int

    def __post_init__(self):
        self._nr_of_waypoints: int = len(self.latitudes)
        lengths = {len(self.timestamps), len(self.latitudes), len(self.longitudes), len(self.headings), len(self.actuator_values)}
        if len(lengths) > 1:
            raise ValueError("All lists must be of equal length.")
        
        # Check if actuator_values is a list of lists or a list of floats
        if all(isinstance(val, list) for val in self.actuator_values):
            # actuator_values is a list of lists
            # Check if the outer list is the same lenght as nr_of_waypoints
            if len(self.actuator_values) != self._nr_of_waypoints:
                raise ValueError(f"The outer list of actuator_values must be of length {self._nr_of_waypoints}. Instead got {len(self.actuator_values)}.")
            
            # Check if all inner lists have the same length as nr_of_actuators
            if any(len(val) != self.nr_of_actuators for val in self.actuator_values):
                raise ValueError(f"All inner lists of actuator_values must be of length {self.nr_of_actuators}, instead got {[len(val) for val in self.actuator_values]}.")
        else:
            # actuator_values is a list of floats
            if self.nr_of_actuators != 1:
                raise ValueError("If actuator_values is a list of floats, nr_of_actuators must be 1.")
            
            if len(self.actuator_values) != len(self._nr_of_waypoints):
                raise ValueError(f"The list of actuator values must be of length {self._nr_of_waypoints}. Instead got {len(self.actuator_values)}.")


@dataclass
class ShipState:
    '''
    Dataclass for representing the state of a ship.

    --------------------------------------------------------------------
    Parameters:

    time (float): In UTC seconds since 1970-01-01 00:00:00
    latitude (float)
    longitude (float)
    heading (float): In radians
    cog (float): Course Over Ground in radians
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
    actuator_values: list
    nr_of_actuators: int


@dataclass
class WindState:
    '''
    Dataclass for representing the state of the wind.

    --------------------------------------------------------------------
    Parameters:

    time: float in UTC seconds since 1970-01-01 00:00:00
    speed: float in m/s
    direction: float in radians
    --------------------------------------------------------------------
    '''
    time: float
    speed: float
    direction: float