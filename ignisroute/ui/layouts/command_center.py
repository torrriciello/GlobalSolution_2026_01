import streamlit as st

from services.analytics_service import compute_operational_metrics
from services.route_orchestrator import analyze_route, export_result_json
from ui.components.alert_banner import render_alert_banner
from ui.components.footer import render_footer
from ui.components.header import render_top_bar
from ui.components.kpi_dashboard import render_kpi_dashboard
from ui.components.map_view import render_map_panel
from ui.components.mission_briefing import render_mission_briefing
from ui.components.operational_intel import render_operational_intel
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
    if not params.main_route:
        st.stop()

    result = analyze_route(
        scenario=params.scenario,
        safety_radius_km=params.radius_km,
        main_route=params.main_route,
        routed_path=params.routed_path,
        origin_label=params.origin_label,
        destination_label=params.destination_label,
    )
    json_path = export_result_json(result)
    metrics = compute_operational_metrics(result.monitored_foci, result.interfering_foci_count)
    mission = build_mission_context(result, metrics, params.radius_km)

    render_top_bar(mission, result.database_connected, result.data_source, params.region_label)
    render_mission_briefing(
        result,
        mission,
        params.radius_km,
        params.origin_label,
        params.destination_label,
    )
    render_kpi_dashboard(result, metrics)
    render_alert_banner(mission)

    map_col, intel_col = st.columns([2.4, 1], gap="medium")

    with map_col:
        render_map_panel(
            result,
            params.radius_km,
            params.origin_label,
            params.destination_label,
        )

    with intel_col:
        render_threat_intel(result, params.radius_km)

    render_operational_intel(result)

    render_footer()
