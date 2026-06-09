import streamlit as st

from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def render_mission_strip(
    result: RouteAnalysisResult,
    mission: MissionContext,
    radius_km: float,
    origin_label: str,
    destination_label: str,
) -> None:
    route_label = "Desvio validado" if result.has_detour else "Rota viária"
    routing_label = "OSRM" if result.routing_source == "osrm" else "Estimada"
    duration = (
        result.detour_duration_min
        if result.has_detour and result.detour_duration_min
        else result.route_duration_min
    )
    decision_class = f"soc-strip-decision--{mission.decision.lower()}"

    st.markdown(
        f"""
        <div class="soc-mission-strip">
            <div class="soc-mission-strip__route">
                <span class="soc-dot soc-dot--origin"></span>
                <span class="soc-mission-strip__path">{origin_label}</span>
                <span class="soc-mission-strip__arrow">→</span>
                <span class="soc-mission-strip__path">{destination_label}</span>
                <span class="soc-dot soc-dot--dest"></span>
            </div>
            <div class="soc-mission-strip__metrics">
                <span><b>{route_label}</b> {result.display_distance:.1f} km</span>
                <span>{duration:.0f} min · {routing_label}</span>
                <span>{result.monitored_foci_count} focos na view</span>
                <span>Margem {radius_km} km</span>
            </div>
            <div class="soc-mission-strip__decision {decision_class}">
                <span class="soc-mission-strip__decision-label">Decisão</span>
                <span class="soc-mission-strip__decision-value">{mission.decision}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
