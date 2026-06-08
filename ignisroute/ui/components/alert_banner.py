import streamlit as st

from ui.mission_context import MissionContext


def render_alert_banner(mission: MissionContext) -> None:
    st.markdown(
        f'<div class="alert-box alert-{mission.alert_type}">{mission.alert_message}</div>',
        unsafe_allow_html=True,
    )
