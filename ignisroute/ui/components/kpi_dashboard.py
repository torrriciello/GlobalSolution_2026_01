import streamlit as st

from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def _metric_card(label: str, value: str, sub: str, css_class: str) -> str:
    return f"""
    <div class="soc-kpi">
        <div class="soc-kpi__label">{label}</div>
        <div class="soc-kpi__value {css_class}">{value}</div>
        <div class="soc-kpi__sub">{sub}</div>
    </div>
    """


def render_kpi_dashboard(result: RouteAnalysisResult, mission: MissionContext) -> None:
    cols = st.columns(6)

    metrics = [
        ("Status da via", result.status_label, "Interdição térmica", result.status_css),
        ("Focos críticos", str(result.interfering_foci_count), "Interferindo na rota", "status-warn"),
        ("Focos monitorados", str(result.monitored_foci_count), "Em observação ativa", "status-info"),
        ("Distância validada", f"{result.display_distance:.1f} km", "Trajeto operacional", "status-info"),
        ("TMR estimado", f"{mission.estimated_response_min:.1f} min", "Tempo de resposta", "status-info"),
        ("Índice de contenção", f"{mission.containment_index:.0f}%", "Rotas seguras", "status-livre"),
    ]

    for col, (label, value, sub, css) in zip(cols, metrics):
        with col:
            st.markdown(_metric_card(label, value, sub, css), unsafe_allow_html=True)
