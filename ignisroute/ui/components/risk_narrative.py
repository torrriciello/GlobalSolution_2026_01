import streamlit as st

from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def _severity_class(severity: str) -> str:
    key = severity.lower().strip()
    if key in {"crítico", "critico"}:
        return "critical"
    if key == "alto":
        return "high"
    return "medium"


def render_risk_narrative(
    result: RouteAnalysisResult,
    mission: MissionContext,
    radius_km: float,
) -> None:
    st.markdown(
        """
        <div class="soc-panel-header">
            <span class="soc-panel-header__title">Narrativa operacional</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="soc-narrative-summary soc-narrative-summary--{mission.alert_type}">
            <div class="soc-narrative-summary__status">{mission.mission_status}</div>
            <div class="soc-narrative-summary__text">{mission.narrative_summary}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="soc-intel-section">Por que esta recomendação?</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="soc-rationale">
            <div class="soc-rationale__action">{mission.decision}</div>
            <div class="soc-rationale__title">{mission.decision_title}</div>
            <div class="soc-rationale__detail">{mission.decision_detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if mission.impact_reasons:
        st.markdown('<div class="soc-intel-section">Impactos críticos na rota</div>', unsafe_allow_html=True)
        for reason in mission.impact_reasons:
            css = _severity_class(reason.severity)
            st.markdown(
                f"""
                <div class="soc-impact-card soc-impact-card--{css}">
                    <div class="soc-impact-card__head">
                        <strong>{reason.title}</strong>
                        <span class="soc-severity soc-severity--{css}">{reason.severity}</span>
                    </div>
                    <div class="soc-impact-card__detail">{reason.detail}</div>
                    <div class="soc-impact-card__meta">
                        <span>Sensor: {reason.sensor}</span>
                        <span>Margem: {radius_km} km</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    elif result.monitored_foci_count > 0:
        st.markdown(
            f"""
            <div class="soc-impact-card soc-impact-card--low">
                <div class="soc-impact-card__detail">
                    {result.monitored_foci_count} foco(s) monitorados na view —
                    nenhum dentro da margem de {radius_km} km da rota viária.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="soc-impact-card soc-impact-card--low">Sem focos ativos na view analítica.</div>',
            unsafe_allow_html=True,
        )
