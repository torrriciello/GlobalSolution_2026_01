import folium
import streamlit as st
from streamlit_folium import st_folium

from maps.map_service import build_route_map
from models.route_result import RouteAnalysisResult


def _prepare_map(result: RouteAnalysisResult, radius_km: float) -> folium.Map:
    map_object = build_route_map(
        route=result.original_route,
        hotspots=result.monitored_foci,
        radius_km=radius_km,
        alt_route=result.detour_route,
        blocked=result.is_blocked,
        validated_route=result.validated_route,
        blocked_hotspots=result.interfering_foci,
    )
    hide_attribution = "<style>.leaflet-control-attribution{display:none!important;}</style>"
    map_object.get_root().header.add_child(folium.Element(hide_attribution))
    return map_object


def render_map_panel(result: RouteAnalysisResult, radius_km: float) -> None:
    st.markdown(
        """
        <div class="soc-panel-header">
            <span class="soc-panel-header__title">🗺️ Mapa Tático</span>
            <span class="soc-panel-header__badge">AO VIVO</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    map_object = _prepare_map(result, radius_km)
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st_folium(map_object, width=None, height=620, returned_objects=[])
    st.markdown("</div>", unsafe_allow_html=True)
