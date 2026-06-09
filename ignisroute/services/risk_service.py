import math
from typing import Dict, List, Tuple

from services.routing_service import fetch_road_alternatives, fetch_road_route
from utils.haversine import distance_km, min_distance_to_route, min_distance_to_route_midsection

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
    (-0.15, 0.15),
    (0.15, -0.12),
    (-0.18, 0.08),
    (0.12, 0.18),
]

IGNORED_STATUSES = {"CONTROLADO", "EXTINTO"}
BLOCKING_STATUS = "ATIVO"
MONITORED_STATUS = "MONITORADO"


def hotspot_status(hotspot: Hotspot) -> str:
    return str(hotspot.get("status_ocorrencia", BLOCKING_STATUS)).strip().upper()


def is_operational_hotspot(hotspot: Hotspot) -> bool:
    return hotspot_status(hotspot) not in IGNORED_STATUSES


def is_blocking_candidate(hotspot: Hotspot) -> bool:
    return hotspot_status(hotspot) == BLOCKING_STATUS


def is_monitored_hotspot(hotspot: Hotspot) -> bool:
    return hotspot_status(hotspot) == MONITORED_STATUS


def filter_operational_hotspots(hotspots: List[Hotspot]) -> List[Hotspot]:
    return [hotspot for hotspot in hotspots if is_operational_hotspot(hotspot)]


def filter_blocking_candidates(hotspots: List[Hotspot]) -> List[Hotspot]:
    return [hotspot for hotspot in hotspots if is_blocking_candidate(hotspot)]


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


def _operational_impact(hotspot: Hotspot) -> str:
    return str(hotspot.get("impacto_operacional", "MONITORAMENTO")).strip().upper()


def _enrich_hotspot_for_detour(hotspot: Hotspot, route: Route, risk_radius_km: float) -> Hotspot:
    lat = hotspot.get("latitude")
    lon = hotspot.get("longitude")

    if lat is None or lon is None:
        return {}

    severity = str(hotspot.get("severity", "Médio"))
    effective_radius = effective_risk_radius(risk_radius_km, severity)
    full_distance = min_distance_to_route(route, (lat, lon))
    mid_distance = min_distance_to_route_midsection(route, (lat, lon))

    return {
        **hotspot,
        "distance_km": round(full_distance, 2),
        "mid_distance_km": round(mid_distance, 2),
        "effective_radius_km": round(effective_radius, 2),
    }


def _invalidates_detour(hotspot: Hotspot) -> bool:
    impact = _operational_impact(hotspot)
    full_distance = float(hotspot.get("distance_km", 0))
    mid_distance = float(hotspot.get("mid_distance_km", full_distance))
    effective_radius = float(hotspot.get("effective_radius_km", 0))

    if impact in {"MONITORAMENTO", "CONTROLADO", "EXTINTO"}:
        return False

    if impact == "DESVIO":
        return mid_distance <= effective_radius

    return full_distance <= effective_radius


def find_risky_hotspots(
    route: Route,
    hotspots: List[Hotspot],
    risk_radius_km: float,
) -> List[Hotspot]:
    risky_hotspots = []

    for hotspot in filter_blocking_candidates(hotspots):
        enriched = enrich_hotspot(hotspot, route, risk_radius_km)
        if not enriched:
            continue
        if is_hotspot_risky(enriched):
            risky_hotspots.append(enriched)

    return sorted(risky_hotspots, key=lambda item: item["distance_km"])


def _route_midpoint(route: Route) -> Tuple[float, float]:
    return route[len(route) // 2]


def _km_to_degree_offsets(latitude: float, radius_km: float) -> Tuple[float, float]:
    lat_deg = radius_km / 111.0
    lon_deg = radius_km / (111.0 * max(math.cos(math.radians(latitude)), 0.25))
    return lat_deg, lon_deg


def _ring_points(
    latitude: float,
    longitude: float,
    radius_km: float,
    step_degrees: int = 30,
    scale: float = 1.0,
) -> List[Tuple[float, float]]:
    lat_deg, lon_deg = _km_to_degree_offsets(latitude, radius_km * scale)
    points: List[Tuple[float, float]] = []

    for angle in range(0, 360, step_degrees):
        radians_angle = math.radians(angle)
        points.append(
            (
                latitude + lat_deg * math.sin(radians_angle),
                longitude + lon_deg * math.cos(radians_angle),
            )
        )

    return points


MAX_SINGLE_VIA_ATTEMPTS = 18
MAX_DOUBLE_VIA_ATTEMPTS = 6


def _avoidance_points_for_hotspot(hotspot: Hotspot, margin_km: float = 2.0) -> List[Tuple[float, float]]:
    latitude = float(hotspot["latitude"])
    longitude = float(hotspot["longitude"])
    radius_km = float(hotspot.get("effective_radius_km", 5.0)) + margin_km

    return _ring_points(latitude, longitude, radius_km, step_degrees=45, scale=1.35)


def _cluster_avoidance_points(blocked_hotspots: List[Hotspot], margin_km: float = 2.5) -> List[Tuple[float, float]]:
    if not blocked_hotspots:
        return []

    latitude = sum(float(hotspot["latitude"]) for hotspot in blocked_hotspots) / len(blocked_hotspots)
    longitude = sum(float(hotspot["longitude"]) for hotspot in blocked_hotspots) / len(blocked_hotspots)
    radius_km = max(float(hotspot.get("effective_radius_km", 5.0)) for hotspot in blocked_hotspots) + margin_km

    points = _ring_points(latitude, longitude, radius_km, step_degrees=45, scale=1.5)
    points.extend(_ring_points(latitude, longitude, radius_km, step_degrees=90, scale=2.0))
    return points


def _build_via_point_candidates(
    route: Route,
    interfering: List[Hotspot],
) -> List[Tuple[float, float]]:
    via_points: List[Tuple[float, float]] = []
    via_points.extend(_cluster_avoidance_points(interfering))

    for hotspot in sorted(interfering, key=lambda item: item.get("distance_km", 0))[:2]:
        via_points.extend(_avoidance_points_for_hotspot(hotspot))

    midpoint = _route_midpoint(route)
    for lat_offset, lon_offset in DETOUR_OFFSETS[:6]:
        via_points.append((midpoint[0] + lat_offset, midpoint[1] + lon_offset))

    deduped: List[Tuple[float, float]] = []
    seen: set[Tuple[float, float]] = set()
    for point in via_points:
        key = (round(point[0], 4), round(point[1], 4))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(point)

    return deduped[:MAX_SINGLE_VIA_ATTEMPTS]


def find_detour_invalid_hotspots(
    route: Route,
    hotspots: List[Hotspot],
    risk_radius_km: float,
) -> List[Hotspot]:
    invalid_hotspots = []

    for hotspot in filter_blocking_candidates(hotspots):
        enriched = _enrich_hotspot_for_detour(hotspot, route, risk_radius_km)
        if not enriched:
            continue
        if _invalidates_detour(enriched):
            invalid_hotspots.append(enriched)

    return sorted(invalid_hotspots, key=lambda item: item["distance_km"])


def _is_route_safe(route: Route, hotspots: List[Hotspot], risk_radius_km: float) -> bool:
    return not find_detour_invalid_hotspots(route, hotspots, risk_radius_km)


def _try_route_candidates(
    origin: Tuple[float, float],
    destination: Tuple[float, float],
    via_points: List[Tuple[float, float]],
    hotspots: List[Hotspot],
    risk_radius_km: float,
) -> Tuple[Route, bool]:
    seen: set[Tuple[float, float]] = set()

    for via_point in via_points:
        key = (round(via_point[0], 4), round(via_point[1], 4))
        if key in seen:
            continue
        seen.add(key)

        candidate = fetch_road_route([origin, via_point, destination])
        if _is_route_safe(candidate.geometry, hotspots, risk_radius_km):
            return candidate.geometry, True

    return [], False


def create_detour_route(
    route: Route,
    hotspots: List[Hotspot],
    risk_radius_km: float,
    blocked_hotspots: List[Hotspot] | None = None,
) -> Tuple[Route, bool]:
    """
    Busca desvio seguro usando rotas alternativas OSRM e waypoints viários
    posicionados ao redor das zonas de exclusão dos focos bloqueantes.
    """
    if len(route) < 2:
        return route, True

    origin = route[0]
    destination = route[-1]
    interfering = blocked_hotspots or find_risky_hotspots(route, hotspots, risk_radius_km)

    for alternative in fetch_road_alternatives(origin, destination):
        if _is_route_safe(alternative.geometry, hotspots, risk_radius_km):
            return alternative.geometry, True

    via_points = _build_via_point_candidates(route, interfering)
    detour, found = _try_route_candidates(origin, destination, via_points, hotspots, risk_radius_km)
    if found:
        return detour, True

    if len(interfering) >= 2:
        primary = _avoidance_points_for_hotspot(interfering[0], margin_km=3.0)[:3]
        secondary = _avoidance_points_for_hotspot(interfering[1], margin_km=3.0)[:3]
        attempts = 0

        for first in primary:
            for second in secondary:
                if attempts >= MAX_DOUBLE_VIA_ATTEMPTS:
                    break
                attempts += 1
                candidate = fetch_road_route([origin, first, second, destination])
                if _is_route_safe(candidate.geometry, hotspots, risk_radius_km):
                    return candidate.geometry, True

    return route, False
