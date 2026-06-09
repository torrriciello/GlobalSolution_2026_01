import streamlit as st

from services.analytics_service import compute_operational_metrics
from services.route_builder import build_mission_route
from services.route_orchestrator import analyze_route, export_result_json
from ui.components.alert_banner import render_alert_banner
from ui.components.footer import render_footer
from ui.components.header import render_top_bar
from ui.components.kpi_dashboard import render_kpi_dashboard
from ui.components.loading_overlay import loading_overlay_html
from ui.components.map_view import render_map_hero
from ui.components.mission_briefing import render_mission_strip
from ui.components.risk_narrative import render_risk_narrative
from ui.components.sidebar import render_sidebar
from ui.components.threat_intel import render_threat_intel
from ui.mission_context import build_mission_context
from ui.styles import CUSTOM_CSS


def _run_analysis(params):
    loader = st.empty()

    loader.markdown(
        loading_overlay_html(
            "Calculando malha viária operacional",
            "Consultando OSRM e traçando rota sobre vias reais…",
        ),
        unsafe_allow_html=True,
    )

    routed = build_mission_route(
        (params.origin_lat, params.origin_lon),
        (params.destination_lat, params.destination_lon),
    )

    loader.markdown(
        loading_overlay_html(
            "Consultando base analítica",
            "Carregando focos ativos de vw_focos_ativos…",
        ),
        unsafe_allow_html=True,
    )

    result = analyze_route(
        scenario=params.scenario,
        safety_radius_km=params.radius_km,
        main_route=routed.geometry,
        routed_path=routed,
        origin_label=params.origin_label,
        destination_label=params.destination_label,
    )

    loader.markdown(
        loading_overlay_html(
            "Montando mapa operacional",
            "Renderizando trajeto, impactos e focos críticos…",
        ),
        unsafe_allow_html=True,
    )

    loader.empty()
    return result


def render_command_center() -> None:
    st.set_page_config(
        page_title="IgnisRoute SOC",
        page_icon="🔥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    params = render_sidebar()
    if not params.ready:
        st.stop()

    result = _run_analysis(params)

    if params.scenario == "Alerta de Queimada" and not result.database_connected:
        st.error(
            "Conexão com PostgreSQL necessária. "
            "Os indicadores e focos devem vir exclusivamente de vw_focos_ativos."
        )

    json_path = export_result_json(result)
    metrics = compute_operational_metrics(result.monitored_foci, result.interfering_foci_count)
    mission = build_mission_context(result, metrics, params.radius_km)

    render_top_bar(mission, result.database_connected, result.data_source, params.region_label)
    render_mission_strip(
        result,
        mission,
        params.radius_km,
        params.origin_label,
        params.destination_label,
    )
    render_kpi_dashboard(result, metrics)

    render_map_hero(
        result,
        params.radius_km,
        params.origin_label,
        params.destination_label,
        mission,
    )

    render_alert_banner(mission)

    narrative_col, intel_col = st.columns([1.35, 1], gap="medium")

    with narrative_col:
        render_risk_narrative(result, mission, params.radius_km)

    with intel_col:
        render_threat_intel(result, params.radius_km)

    render_footer()
