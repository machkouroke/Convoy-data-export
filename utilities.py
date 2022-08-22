import math

import pandas as pd

ROUTE_LENGTH = 450


def was_were(number_of_rows: int) -> str:
    """
    Returns "was" if number_of_rows is 1, otherwise "were"
    """
    return " was" if number_of_rows == 1 else "s were"


def pit_stops(vehicle: pd.Series) -> float:
    """
    Returns the number of pit stops for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: The number of pit stops for the vehicle rounded to the nearest integer
    """
    return math.floor(fuel_consumed(vehicle) / vehicle["engine_capacity"])


def fuel_consumed(vehicle: pd.Series) -> float:
    """
    Returns the fuel consumed for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: Fuel consumed for the vehicle
    """
    return (ROUTE_LENGTH / 100) * vehicle["fuel_consumption"]


def pit_stops_score(vehicle: pd.Series) -> int:
    """
    Returns the pit stops score for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: The pit stops score for the vehicle
    """
    if pit_stops(vehicle) >= 2:
        return 0
    elif pit_stops(vehicle) == 1:
        return 1
    else:
        return 2


def fuel_consumption_score(vehicle: pd.Series) -> int:
    """
    Returns the fuel consumption score for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: The fuel consumption score for the vehicle
    """
    return 2 if fuel_consumed(vehicle) <= 230 else 1


def truck_capacity_score(vehicle: pd.Series) -> int:
    """
    Returns the truck capacity score for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: The truck capacity score for the vehicle
    """
    return 2 if vehicle["maximum_load"] >= 20 else 0


def scores(vehicle: pd.Series) -> int:
    """
    Returns the score for a vehicle
    :param vehicle: A pandas series with the vehicle data
    :return: returns the score for the vehicle. The score is the sum of the scores for the pit stops,
    fuel consumption and truck capacity
    """
    return sum([pit_stops_score(vehicle),
                fuel_consumption_score(vehicle),
                truck_capacity_score(vehicle)])
