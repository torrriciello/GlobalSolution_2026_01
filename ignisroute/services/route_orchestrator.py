import json

from pathlib import Path
from typing import Optional

from maps.map_service import (
    build_route_map,
    export_map_html,
)

from models.route_result import (
    Route,
    RouteAnalysisResult,
)

from services.hotspot_repository import load_hotspots

from services.risk_service import (
    create_detour_route,
    effective_risk_radius,
    find_risky_hotspots,
    get_route_distance_km,
)

from utils.haversine import min_distance_to_route


DEFAULT_ROUTE: Route = [
    (-23.5048, -46.6299),
    (-23.5505, -46.6333),
    (-23.5934, -46.6305),
]

FREE_ROUTE_SCENARIOS = {
    "via livre",
    "livre",
    "clear",
}

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def annotate_hotspots(
    hotspots: list,
    route: Route,
    safety_radius_km: float,
) -> list:
    """
    Enriquece os focos com métricas operacionais.
    """

    annotated = []

    for hotspot in hotspots:

        lat = hotspot.get("latitude")
        lon = hotspot.get("longitude")

        if lat is None or lon is None:
            continue

        entry = hotspot.copy()

        entry["distance_km"] = round(
            min_distance_to_route(
                route,
                (lat, lon),
            ),
            2,
        )

        entry["effective_radius_km"] = round(
            effective_risk_radius(
                safety_radius_km,
                str(
                    hotspot.get(
                        "severity",
                        "Médio",
                    )
                ),
            ),
            2,
        )

        annotated.append(entry)

    return annotated


def export_analysis_map(
    route: Route,
    hotspots: list,
    safety_radius_km: float,
    blocked: bool,
    validated_route: Route,
    detour_route: Optional[Route],
    blocked_hotspots: list,
) -> str | None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    map_object = build_route_map(
        route=route,
        hotspots=hotspots,
        radius_km=safety_radius_km,
        alt_route=detour_route,
        blocked=blocked,
        validated_route=validated_route,
        blocked_hotspots=blocked_hotspots,
    )

    output_file = OUTPUT_DIR / "rota_tatica.html"

    export_map_html(
        map_object,
        str(output_file),
    )

    return str(output_file)


def analyze_route(
    scenario: str,
    safety_radius_km: float,
    main_route: Optional[Route] = None,
    export_html: bool = True,
) -> RouteAnalysisResult:
    """
    Executa a análise completa da rota.
    """

    route = main_route or DEFAULT_ROUTE

    hotspot_load = load_hotspots()
    hotspots = hotspot_load.hotspots
    connected = hotspot_load.connected

    if scenario.strip().lower() in FREE_ROUTE_SCENARIOS:
        hotspots = []

    annotated_hotspots = annotate_hotspots(
        hotspots,
        route,
        safety_radius_km,
    )

    blocked_hotspots = find_risky_hotspots(
        route,
        hotspots,
        safety_radius_km,
    )

    blocked = bool(blocked_hotspots)

    detour_route = None
    detour_found = True

    if blocked:

        detour_route, detour_found = (
            create_detour_route(
                route,
                hotspots,
                safety_radius_km,
            )
        )

    validated_route = (
        detour_route
        if blocked
        and detour_found
        and detour_route
        else route
    )

    road_status = (
        "INTERDITADA"
        if blocked
        else "LIVRE"
    )

    map_html_path = None

    if export_html:

        map_html_path = export_analysis_map(
            route=route,
            hotspots=hotspots,
            safety_radius_km=safety_radius_km,
            blocked=blocked,
            validated_route=validated_route,
            detour_route=detour_route,
            blocked_hotspots=blocked_hotspots,
        )

    return RouteAnalysisResult(
        road_status=road_status,
        interfering_foci_count=len(blocked_hotspots),
        monitored_foci_count=len(hotspots),
        validated_route=validated_route,
        original_route=route,
        detour_route=detour_route,
        interfering_foci=blocked_hotspots,
        monitored_foci=annotated_hotspots,
        scenario=scenario,
        safety_radius_km=safety_radius_km,
        route_distance_km=round(
            get_route_distance_km(route),
            2,
        ),
        detour_distance_km=(
            round(
                get_route_distance_km(
                    detour_route
                ),
                2,
            )
            if detour_route
            else None
        ),
        database_connected=connected,
        data_source=hotspot_load.source,
        connection_error=hotspot_load.error,
        map_html_path=map_html_path,
        detour_found=detour_found,
    )


def export_result_json(
    result: RouteAnalysisResult,
    path: Optional[str] = None,
) -> str:
    """
    Exporta o resultado da análise para JSON.
    """

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path = (
        Path(path)
        if path
        else OUTPUT_DIR / "analise_rota.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            result.to_dict(),
            file,
            ensure_ascii=False,
            indent=2,
        )

    return str(output_path)