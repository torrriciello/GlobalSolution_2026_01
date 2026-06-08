import streamlit as st

from ui.constants import APP_VERSION


def render_footer() -> None:
    st.markdown(
        f"""
        <div class="soc-footer">
            <span>IgnisRoute SOC v{APP_VERSION}</span>
            <span>Global Solution FIAP 2026</span>
            <span>Haversine · PostgreSQL · Folium · Supabase</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
