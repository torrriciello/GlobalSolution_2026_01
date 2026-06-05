from typing import Dict, List, Tuple
from utils.haversine import distance_km, min_distance_to_route

Route = List[Tuple[float, float]]
Hotspot = Dict[str, object]


def get_route_distance_km(route: Route) -> float:
    return sum(
        distance_km(route[index], route[index + 1])
        for index in range(len(route) - 1)
    )


def find_risky_hotspots(route: Route, hotspots: List[Hotspot], risk_radius_km: float) -> List[Hotspot]:
    result = []
    for hotspot in hotspots:
        location = (hotspot.get("latitude"), hotspot.get("longitude"))
        if location[0] is None or location[1] is None:
            continue
        distance = min_distance_to_route(route, location)
        hotspot_result = hotspot.copy()
        hotspot_result["distance_km"] = round(distance, 2)
        if distance <= risk_radius_km:
            result.append(hotspot_result)
    return sorted(result, key=lambda item: item["distance_km"])


def create_detour_route(route: Route) -> Route:
    if len(route) < 3:
        return route

    origin = route[0]
    destination = route[-1]
    midpoint = route[len(route) // 2]
    shifted_midpoint = (midpoint[0] - 0.07, midpoint[1] + 0.10)

    return [origin, shifted_midpoint, destination]
