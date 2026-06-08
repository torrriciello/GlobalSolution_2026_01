from typing import Dict, List, Tuple

from services.routing_service import fetch_road_alternatives, fetch_road_route
from utils.haversine import distance_km, min_distance_to_route

Route = List[Tuple[float, float]]
Hotspot = Dict[str, object]


SEVERITY_MULTIPLIER = {
    "alto": 1.25,
    "médio": 1.0,
    "medio": 1.0,
    "baixo": 0.85,
    "crítico": 1.35,
    "critico": 1.35,
}

DETOUR_OFFSETS = [
    (-0.07, 0.10),
    (-0.10, 0.07),
    (-0.05, 0.12),
    (0.07, 0.10),
    (-0.08, -0.08),
    (0.10, -0.05),
    (-0.12, 0.05),
    (0.05, 0.12),
]


def get_route_distance_km(route: Route) -> float:
    if len(route) < 2:
        return 0.0

    return sum(
        distance_km(route[index], route[index + 1])
        for index in range(len(route) - 1)
    )


def effective_risk_radius(base_radius_km: float, severity: str) -> float:
    multiplier = SEVERITY_MULTIPLIER.get(severity.lower().strip(), 1.0)
    return base_radius_km * multiplier


def enrich_hotspot(hotspot: Hotspot, route: Route, risk_radius_km: float) -> Hotspot:
    lat = hotspot.get("latitude")
    lon = hotspot.get("longitude")

    if lat is None or lon is None:
        return {}

    severity = str(hotspot.get("severity", "Médio"))
    distance = min_distance_to_route(route, (lat, lon))
    effective_radius = effective_risk_radius(risk_radius_km, severity)

    return {
        **hotspot,
        "distance_km": round(distance, 2),
        "effective_radius_km": round(effective_radius, 2),
    }


def is_hotspot_risky(hotspot: Hotspot) -> bool:
    return hotspot["distance_km"] <= hotspot["effective_radius_km"]


def find_risky_hotspots(
    route: Route,
    hotspots: List[Hotspot],
    risk_radius_km: float,
) -> List[Hotspot]:
    risky_hotspots = []

    for hotspot in hotspots:
        enriched = enrich_hotspot(hotspot, route, risk_radius_km)
        if not enriched:
            continue
        if is_hotspot_risky(enriched):
            risky_hotspots.append(enriched)

    return sorted(risky_hotspots, key=lambda item: item["distance_km"])


def _route_midpoint(route: Route) -> Tuple[float, float]:
    return route[len(route) // 2]


def _is_route_safe(route: Route, hotspots: List[Hotspot], risk_radius_km: float) -> bool:
    return not find_risky_hotspots(route, hotspots, risk_radius_km)


def create_detour_route(
    route: Route,
    hotspots: List[Hotspot],
    risk_radius_km: float,
) -> Tuple[Route, bool]:
    """
    Busca desvio seguro usando rotas alternativas OSRM e waypoints viários.
    """
    if len(route) < 2:
        return route, True

    origin = route[0]
    destination = route[-1]

    for alternative in fetch_road_alternatives(origin, destination):
        if _is_route_safe(alternative.geometry, hotspots, risk_radius_km):
            return alternative.geometry, True

    midpoint = _route_midpoint(route)
    for lat_offset, lon_offset in DETOUR_OFFSETS:
        via_point = (midpoint[0] + lat_offset, midpoint[1] + lon_offset)
        candidate = fetch_road_route([origin, via_point, destination])
        if _is_route_safe(candidate.geometry, hotspots, risk_radius_km):
            return candidate.geometry, True

    return route, False
