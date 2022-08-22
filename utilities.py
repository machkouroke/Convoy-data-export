import math

import pandas as pd

ROUTE_LENGTH = 450


def log_score(f):
    def wrapper(*args, **kwargs):
        score = f(*args, **kwargs)
        print(f"{f.__name__} score: {score}", file=open("scores.txt", "a"))
        return score

    return wrapper


@log_score
def test(ok):
    return ok


def was_were(number_of_rows: int) -> str:
    return " was" if number_of_rows == 1 else "s were"


def pit_stops(vehicle: pd.Series) -> float:
    return math.floor(fuel_consumed(vehicle) / vehicle["engine_capacity"])


def fuel_consumed(vehicle: pd.Series) -> float:
    return (ROUTE_LENGTH / 100) * vehicle["fuel_consumption"]


@log_score
def pit_stops_score(vehicle: pd.Series) -> int:
    if pit_stops(vehicle) >= 2:
        return 0
    elif pit_stops(vehicle) == 1:
        return 1
    else:
        return 2


@log_score
def fuel_consumption_score(vehicle: pd.Series) -> int:
    return 2 if fuel_consumed(vehicle) <= 230 else 1


@log_score
def truck_capacity_score(vehicle: pd.Series) -> int:
    return 2 if vehicle["maximum_load"] >= 20 else 0


def scores(vehicle: pd.Series) -> int:
    return sum([pit_stops_score(vehicle),
                fuel_consumption_score(vehicle),
                truck_capacity_score(vehicle)])
