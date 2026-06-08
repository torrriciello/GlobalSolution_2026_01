import folium
import streamlit as st
from streamlit_folium import st_folium

from maps.map_service import build_route_map
from models.route_result import RouteAnalysisResult


def _prepare_map(
    result: RouteAnalysisResult,
    radius_km: float,
    origin_label: str,
    destination_label: str,
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
    )
    hide_attribution = "<style>.leaflet-control-attribution{display:none!important;}</style>"
    map_object.get_root().header.add_child(folium.Element(hide_attribution))
    return map_object


def render_map_panel(
    result: RouteAnalysisResult,
    radius_km: float,
    origin_label: str,
    destination_label: str,
) -> None:
    routing_label = "Malha viária OSRM" if result.routing_source == "osrm" else "Trajeto estimado"
    route_points = len(result.validated_route)

    st.markdown(
        f"""
        <div class="soc-panel-header soc-panel-header--map">
            <div>
                <span class="soc-panel-header__title">Mapa operacional</span>
                <span class="soc-panel-header__caption">{routing_label} · {route_points} pontos de trajeto</span>
            </div>
            <span class="soc-panel-header__badge soc-panel-header__badge--live">AO VIVO</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    map_object = _prepare_map(result, radius_km, origin_label, destination_label)
    st.markdown('<div class="map-container map-container--hero">', unsafe_allow_html=True)
    st_folium(map_object, width=None, height=680, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)
