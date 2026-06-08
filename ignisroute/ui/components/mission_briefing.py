import streamlit as st

from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def render_mission_briefing(
    result: RouteAnalysisResult,
    mission: MissionContext,
    radius_km: float,
    origin_label: str,
    destination_label: str,
) -> None:
    decision_class = f"soc-decision--{mission.decision.lower()}"
    route_label = "Desvio validado" if result.has_detour else "Rota viária validada"
    routing_label = "OSRM" if result.routing_source == "osrm" else "Estimada"
    duration = result.detour_duration_min if result.has_detour and result.detour_duration_min else result.route_duration_min
    extra_km = 0.0
    if result.detour_distance_km:
        extra_km = max(result.detour_distance_km - result.route_distance_km, 0)

    st.markdown(
        f"""
        <div class="soc-mission-grid">
            <div class="soc-panel soc-panel--briefing">
                <div class="soc-panel__label">CONTEXTO DA MISSÃO</div>
                <div class="soc-panel__title">{mission.mission_status}</div>
                <div class="soc-mission-route">
                    <div class="soc-mission-route__point">
                        <span class="soc-dot soc-dot--origin"></span>
                        <div>
                            <div class="soc-mission-route__label">Origem</div>
                            <div class="soc-mission-route__value">{origin_label}</div>
                        </div>
                    </div>
                    <div class="soc-mission-route__line"></div>
                    <div class="soc-mission-route__point">
                        <span class="soc-dot soc-dot--dest"></span>
                        <div>
                            <div class="soc-mission-route__label">Destino</div>
                            <div class="soc-mission-route__value">{destination_label}</div>
                        </div>
                    </div>
                </div>
                <div class="soc-mission-meta">
                    <span>🛣️ {route_label}: {result.display_distance:.1f} km</span>
                    <span>⏱️ {duration:.0f} min · {routing_label}</span>
                    <span>📡 {result.scenario}</span>
                    <span>⭕ Margem {radius_km} km</span>
                    {"<span>↗️ +" + f"{extra_km:.1f}" + " km no desvio</span>" if extra_km > 0 else ""}
                </div>
            </div>
            <div class="soc-panel soc-panel--decision {decision_class}">
                <div class="soc-panel__label">RECOMENDAÇÃO TÁTICA</div>
                <div class="soc-decision-action">{mission.decision}</div>
                <div class="soc-decision-title">{mission.decision_title}</div>
                <div class="soc-decision-detail">{mission.decision_detail}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
