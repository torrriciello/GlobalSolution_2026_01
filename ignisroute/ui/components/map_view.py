import folium
import streamlit as st
from streamlit_folium import st_folium

from maps.map_service import build_route_map
from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def _prepare_map(
    result: RouteAnalysisResult,
    radius_km: float,
    origin_label: str,
    destination_label: str,
    mission: MissionContext,
) -> folium.Map:
    map_object = build_route_map(
        route=result.original_route,
        hotspots=result.monitored_foci,
        radius_km=radius_km,
        alt_route=result.detour_route,
        blocked=result.is_blocked,
        validated_route=result.validated_route,
        blocked_hotspots=result.interfering_foci,
        origin_label=origin_label,
        destination_label=destination_label,
        routing_source=result.routing_source,
        mission_status=mission.mission_status,
        route_km=result.display_distance,
        detour_found=result.detour_found,
    )
    hide_attribution = "<style>.leaflet-control-attribution{display:none!important;}</style>"
    map_object.get_root().header.add_child(folium.Element(hide_attribution))
    return map_object


def render_map_hero(
    result: RouteAnalysisResult,
    radius_km: float,
    origin_label: str,
    destination_label: str,
    mission: MissionContext,
) -> None:
    routing_label = "Malha viária OSRM" if result.routing_source == "osrm" else "Trajeto estimado"
    critical_label = (
        f"{result.interfering_foci_count} foco(s) crítico(s) na rota"
        if result.interfering_foci_count
        else "Nenhum impacto crítico na margem configurada"
    )

    st.markdown(
        f"""
        <div class="map-hero-head">
            <div>
                <div class="map-hero-head__title">Centro de operações geoespaciais</div>
                <div class="map-hero-head__sub">{origin_label} → {destination_label}</div>
            </div>
            <div class="map-hero-head__meta">
                <span class="map-hero-chip map-hero-chip--route">{routing_label}</span>
                <span class="map-hero-chip map-hero-chip--{'danger' if result.is_blocked else 'safe'}">
                    {critical_label}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    map_object = _prepare_map(result, radius_km, origin_label, destination_label, mission)

    st_folium(
        map_object,
        use_container_width=True,
        height=720,
        returned_objects=[]
    )
