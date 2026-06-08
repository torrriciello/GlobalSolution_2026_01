"""Motor de roteamento viário — malha rodoviária via OSRM."""

import logging
import os
from dataclasses import dataclass

import requests
from dotenv import load_dotenv

from utils.haversine import distance_km, interpolate_point

load_dotenv()

logger = logging.getLogger(__name__)

Coordinate = tuple[float, float]
Route = list[Coordinate]

DEFAULT_OSRM_URL = "https://router.project-osrm.org"
OSRM_BASE_URL = os.getenv("OSRM_URL", DEFAULT_OSRM_URL).rstrip("/")
REQUEST_TIMEOUT = int(os.getenv("OSRM_TIMEOUT", "12"))


@dataclass
class RoutedPath:
    geometry: Route
    distance_km: float
    duration_min: float
    source: str


def _coords_to_osrm(waypoints: list[Coordinate]) -> str:
    return ";".join(f"{lon:.6f},{lat:.6f}" for lat, lon in waypoints)


def _decode_geojson_line(geojson: dict) -> Route:
    coordinates = geojson.get("coordinates", [])
    return [(lat, lon) for lon, lat in coordinates]


def _fallback_geometry(waypoints: list[Coordinate], steps_per_segment: int = 40) -> Route:
    if len(waypoints) < 2:
        return waypoints

    geometry: Route = []
    for index in range(len(waypoints) - 1):
        start = waypoints[index]
        end = waypoints[index + 1]
        segment_steps = steps_per_segment if index < len(waypoints) - 2 else steps_per_segment + 1

        for step in range(segment_steps):
            ratio = step / steps_per_segment
            geometry.append(interpolate_point(start, end, ratio))

    geometry.append(waypoints[-1])
    return geometry


def _fallback_path(waypoints: list[Coordinate]) -> RoutedPath:
    geometry = _fallback_geometry(waypoints)
    total_km = sum(
        distance_km(geometry[i], geometry[i + 1])
        for i in range(len(geometry) - 1)
    )
    duration_min = (total_km / 50) * 60 if total_km else 0.0

    return RoutedPath(
        geometry=geometry,
        distance_km=round(total_km, 2),
        duration_min=round(duration_min, 1),
        source="fallback",
    )


def _parse_osrm_route(route_data: dict, source: str = "osrm") -> RoutedPath:
    geometry = _decode_geojson_line(route_data["geometry"])
    distance_km = float(route_data.get("distance", 0)) / 1000
    duration_min = float(route_data.get("duration", 0)) / 60

    return RoutedPath(
        geometry=geometry,
        distance_km=round(distance_km, 2),
        duration_min=round(duration_min, 1),
        source=source,
    )


def _request_routes(waypoints: list[Coordinate], alternatives: bool = False) -> list[RoutedPath]:
    if len(waypoints) < 2:
        return [_fallback_path(waypoints)]

    coord_path = _coords_to_osrm(waypoints)
    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }
    if alternatives and len(waypoints) == 2:
        params["alternatives"] = "true"

    url = f"{OSRM_BASE_URL}/route/v1/driving/{coord_path}"

    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        payload = response.json()

        if payload.get("code") != "Ok" or not payload.get("routes"):
            logger.warning("OSRM sem rotas válidas: %s", payload.get("message", payload.get("code")))
            return [_fallback_path(waypoints)]

        return [_parse_osrm_route(route) for route in payload["routes"]]

    except requests.RequestException as error:
        logger.warning("OSRM indisponível (%s) — usando fallback geométrico.", error)
        return [_fallback_path(waypoints)]


def fetch_road_route(waypoints: list[Coordinate]) -> RoutedPath:
    """Calcula rota viária passando pelos waypoints informados."""
    routes = _request_routes(waypoints, alternatives=False)
    return routes[0]


def fetch_road_alternatives(origin: Coordinate, destination: Coordinate) -> list[RoutedPath]:
    """Retorna rotas alternativas entre origem e destino."""
    return _request_routes([origin, destination], alternatives=True)


def find_safe_alternative(
    origin: Coordinate,
    destination: Coordinate,
    is_safe,
) -> RoutedPath | None:
    """
    Busca a primeira rota alternativa que satisfaça a função de segurança.
    `is_safe` recebe a geometria da rota e retorna bool.
    """
    for candidate in fetch_road_alternatives(origin, destination):
        if is_safe(candidate.geometry):
            return candidate
    return None
