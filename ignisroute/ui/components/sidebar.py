from dataclasses import dataclass

import streamlit as st

from ui.constants import SCENARIOS


@dataclass
class OperationParams:
    scenario: str
    radius_km: float
    show_threats: bool
    show_json: bool


def render_sidebar() -> OperationParams:
    with st.sidebar:
        st.markdown(
            """
            <div class="soc-sidebar-header">
                <div class="soc-sidebar-header__icon">⚙️</div>
                <div>
                    <div class="soc-sidebar-header__title">Painel de Controle</div>
                    <div class="soc-sidebar-header__sub">Parâmetros da missão</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="soc-sidebar-section">Cenário operacional</div>', unsafe_allow_html=True)
        scenario = st.selectbox(
            "Cenário",
            SCENARIOS,
            index=1,
            label_visibility="collapsed",
            help="Define se focos de calor ativos entram na análise de risco.",
        )

        st.markdown('<div class="soc-sidebar-section">Tolerância térmica</div>', unsafe_allow_html=True)
        radius_km = st.slider(
            "Raio de segurança (km)",
            min_value=1,
            max_value=15,
            value=5,
            step=1,
            label_visibility="collapsed",
            help="Distância mínima entre a rota e cada zona de exclusão.",
        )

        st.markdown(
            f'<div class="soc-radius-display">Raio ativo: <strong>{radius_km} km</strong></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown('<div class="soc-sidebar-section">Exibição</div>', unsafe_allow_html=True)
        show_threats = st.toggle("Painel de ameaças", value=True)
        show_json = st.toggle("Dados estruturados (JSON)", value=False)

        st.markdown("---")

    return OperationParams(
        scenario=scenario,
        radius_km=radius_km,
        show_threats=show_threats,
        show_json=show_json,
    )
