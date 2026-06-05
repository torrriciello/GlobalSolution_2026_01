from math import atan2, cos, radians, sin, sqrt
from typing import Iterable, Tuple

Coordinates = Tuple[float, float]


def distance_km(origin: Coordinates, destination: Coordinates) -> float:
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371.0

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return radius * c


def min_distance_to_route(route: Iterable[Coordinates], point: Coordinates, steps: int = 20) -> float:
    route_list = list(route)
    min_distance = float("inf")
    for index in range(len(route_list) - 1):
        start = route_list[index]
        end = route_list[index + 1]
        for step in range(steps + 1):
            ratio = step / steps
            intermediate = (
                start[0] + (end[0] - start[0]) * ratio,
                start[1] + (end[1] - start[1]) * ratio,
            )
            min_distance = min(min_distance, distance_km(intermediate, point))
    return min_distance
