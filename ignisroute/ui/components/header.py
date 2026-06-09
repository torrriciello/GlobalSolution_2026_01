import streamlit as st

from ui.constants import APP_TITLE, APP_VERSION
from ui.mission_context import MissionContext, current_timestamp


def render_top_bar(
    mission: MissionContext,
    db_connected: bool,
    data_source: str,
    region_label: str,
) -> None:
    if db_connected:
        label = {
            "postgresql": "POSTGRESQL",
            "supabase": "SUPABASE REST",
        }.get(data_source, data_source.upper())
        db_badge = f'<span class="soc-badge soc-badge--online">● {label}</span>'
    else:
        db_badge = '<span class="soc-badge soc-badge--offline">● MODO DEMONSTRAÇÃO</span>'

    risk_class = f"soc-risk--{mission.risk_level.lower()}"

    st.markdown(
        f"""
        <div class="soc-topbar">
            <div class="soc-topbar__brand">
                <span class="soc-topbar__logo">🔥</span>
                <div>
                    <div class="soc-topbar__title">{APP_TITLE}</div>
                    <div class="soc-topbar__subtitle">Centro de Operações Geoespaciais · v{APP_VERSION}</div>
                </div>
            </div>
            <div class="soc-topbar__center">
                <span class="soc-topbar__region">📍 {region_label}</span>
            </div>
            <div class="soc-topbar__status">
                {db_badge}
                <span class="soc-badge {risk_class}">RISCO {mission.risk_level}</span>
                <span class="soc-topbar__clock">{current_timestamp()}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
