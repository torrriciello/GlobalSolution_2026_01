from math import atan2, cos, radians, sin, sqrt
from typing import Iterable, Tuple

Coordinates = Tuple[float, float]

EARTH_RADIUS_KM = 6371.0


def distance_km(origin: Coordinates, destination: Coordinates) -> float:
    """
    Calcula a distância geodésica entre dois pontos utilizando
    a fórmula de Haversine.

    Args:
        origin: (latitude, longitude)
        destination: (latitude, longitude)

    Returns:
        Distância em quilômetros.
    """

    lat1, lon1 = origin
    lat2, lon2 = destination

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = (
        sin(dlat / 2) ** 2
        + cos(radians(lat1))
        * cos(radians(lat2))
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def interpolate_point(
    start: Coordinates,
    end: Coordinates,
    ratio: float,
) -> Coordinates:
    """
    Retorna um ponto intermediário entre dois pontos.
    """

    return (
        start[0] + (end[0] - start[0]) * ratio,
        start[1] + (end[1] - start[1]) * ratio,
    )


def min_distance_to_route(
    route: Iterable[Coordinates],
    point: Coordinates,
    steps_per_segment: int = 100,
) -> float:
    """
    Calcula a menor distância aproximada entre um ponto e uma rota.

    A rota é discretizada em vários pontos intermediários,
    aumentando significativamente a precisão da medição.

    Args:
        route:
            Lista de coordenadas da rota.

        point:
            Ponto de referência.

        steps_per_segment:
            Quantidade de amostras por segmento.

    Returns:
        Menor distância encontrada em quilômetros.
    """

    route_points = list(route)

    if len(route_points) < 2:
        return float("inf")

    min_distance = float("inf")

    for i in range(len(route_points) - 1):

        start = route_points[i]
        end = route_points[i + 1]

        for step in range(steps_per_segment + 1):

            ratio = step / steps_per_segment

            candidate = interpolate_point(
                start,
                end,
                ratio,
            )

            distance = distance_km(
                candidate,
                point,
            )

            if distance < min_distance:
                min_distance = distance

    return round(min_distance, 3)


def min_distance_to_route_midsection(
    route: Iterable[Coordinates],
    point: Coordinates,
    trim_fraction: float = 0.15,
    steps_per_segment: int = 100,
) -> float:
    """
    Mede a menor distância ao trecho central da rota, ignorando
    os extremos próximos à origem e ao destino operacionais.
    """
    route_points = list(route)

    if len(route_points) < 4:
        return min_distance_to_route(route, point, steps_per_segment)

    start_index = max(1, int(len(route_points) * trim_fraction))
    end_index = min(len(route_points) - 1, int(len(route_points) * (1 - trim_fraction)))

    if start_index >= end_index:
        return min_distance_to_route(route, point, steps_per_segment)

    return min_distance_to_route(
        route_points[start_index:end_index],
        point,
        steps_per_segment,
    )


def closest_point_on_route(
    route: Iterable[Coordinates],
    point: Coordinates,
    steps_per_segment: int = 100,
) -> Tuple[Coordinates, float]:
    """
    Retorna o ponto mais próximo na rota e a distância em km.
    """
    route_points = list(route)

    if len(route_points) < 2:
        return point, float("inf")

    closest = route_points[0]
    min_distance = float("inf")

    for i in range(len(route_points) - 1):
        start = route_points[i]
        end = route_points[i + 1]

        for step in range(steps_per_segment + 1):
            ratio = step / steps_per_segment
            candidate = interpolate_point(start, end, ratio)
            distance = distance_km(candidate, point)

            if distance < min_distance:
                min_distance = distance
                closest = candidate

    return closest, round(min_distance, 3)