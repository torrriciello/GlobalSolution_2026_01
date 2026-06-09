"""Overlay de carregamento para operações longas (OSRM + análise)."""


def loading_overlay_html(step: str, detail: str = "") -> str:
    detail_html = f'<div class="soc-loader__detail">{detail}</div>' if detail else ""
    return f"""
    <div class="soc-loader">
        <div class="soc-loader__card">
            <div class="soc-loader__spinner"></div>
            <div class="soc-loader__title">IgnisRoute SOC</div>
            <div class="soc-loader__step">{step}</div>
            {detail_html}
            <div class="soc-loader__bar"><div class="soc-loader__bar-fill"></div></div>
        </div>
    </div>
    """


def render_loading_screen(step: str, detail: str = "") -> None:
    import streamlit as st

    st.markdown(loading_overlay_html(step, detail), unsafe_allow_html=True)
