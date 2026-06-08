import streamlit as st

from services.route_orchestrator import analyze_route, export_result_json
from ui.components.alert_banner import render_alert_banner
from ui.components.export_panel import render_export_panel
from ui.components.footer import render_footer
from ui.components.header import render_top_bar
from ui.components.kpi_dashboard import render_kpi_dashboard
from ui.components.map_view import render_map_panel
from ui.components.mission_briefing import render_mission_briefing
from ui.components.sidebar import render_sidebar
from ui.components.threat_intel import render_threat_intel
from ui.mission_context import build_mission_context
from ui.styles import CUSTOM_CSS


def render_command_center() -> None:
    st.set_page_config(
        page_title="IgnisRoute SOC",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    params = render_sidebar()
    result = analyze_route(scenario=params.scenario, safety_radius_km=params.radius_km)
    json_path = export_result_json(result)
    mission = build_mission_context(result, params.radius_km)

    render_top_bar(mission, result.database_connected, result.data_source)
    render_mission_briefing(result, mission, params.radius_km)
    render_kpi_dashboard(result, mission)
    render_alert_banner(mission)

    map_col, intel_col = st.columns([2.2, 1], gap="medium")

    with map_col:
        render_map_panel(result, params.radius_km)

    with intel_col:
        if params.show_threats:
            render_threat_intel(result, mission, params.radius_km)
        render_export_panel(result, json_path)

    if params.show_json:
        st.markdown('<p class="section-title">📋 Saída estruturada</p>', unsafe_allow_html=True)
        with st.expander("Payload completo da análise", expanded=False):
            st.json(result.to_dict())

    render_footer()
