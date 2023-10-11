from dataclasses import dataclass


@dataclass
class Trajectory:
    '''
    Dataclass for representing a trajectory.
    The trajectory consists of a list of latitudes, a list of longitudes, a list of actuator values, and a list of timestamps.
    All lists must be of equal length.

    latitudes: list of floats
    longitudes: list of floats
    actuator_values: list of floats or list of lists of floats
    timestamps: list of floats in UTC seconds since 1970-01-01 00:00:00
    nr_of_actuators: int
    '''
    latitudes: list
    longitudes: list
    actuator_values: list
    timestamps: list
    nr_of_actuators: int
    _nr_of_waypoints: int = len(latitudes)

    def __post_init__(self):
        lengths = {len(self.latitudes), len(self.longitudes), len(self.actuator_values), len(self.timestamps)}
        if len(lengths) > 1:
            raise ValueError("All lists must be of equal length.")
        
        # Check if actuator_values is a list of lists or a list of floats
        if all(isinstance(val, list) for val in self.actuator_values):
            # actuator_values is a list of lists
            if len(self.actuator_values) != len(self.nr_of_actuators):
                raise ValueError("The number of actuators is inconsistent with the list of actuator values.")
            
            # Check if all inner lists have the same length as _nr_of_waypoints
            if any(len(val) != self._nr_of_waypoints for val in self.actuator_values):
                raise ValueError(f"All inner lists in actuator_values must be of length {self._nr_of_waypoints}. Instead got {[len(val) for val in self.actuator_values]}.")
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

    latitude: float
    longitude: float
    heading: float in radians
    COG: float in radians
    SOG: float in m/s
    time: float in UTC seconds since 1970-01-01 00:00:00
    '''
    latitude: float
    longitude: float
    heading: float
    COG: float
    SOG: float
    time: float


@dataclass
class WindState:
    '''
    Dataclass for representing the state of the wind.

    direction: float in radians
    speed: float in m/s
    time: float in UTC seconds since 1970-01-01 00:00:00
    '''
    direction: float
    speed: float
    time: float