import streamlit as st

from models.route_result import RouteAnalysisResult
from ui.mission_context import MissionContext


def _severity_badge(severity: str) -> str:
    key = str(severity).lower().strip()
    css = {"alto": "high", "médio": "medium", "medio": "medium", "baixo": "low"}.get(key, "medium")
    return f'<span class="soc-severity soc-severity--{css}">{severity}</span>'


def render_threat_intel(result: RouteAnalysisResult, mission: MissionContext, radius_km: float) -> None:
    st.markdown(
        """
        <div class="soc-panel-header">
            <span class="soc-panel-header__title">🎯 Inteligência de Ameaças</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="soc-intel-summary">
            <div class="soc-intel-stat">
                <div class="soc-intel-stat__val">{result.interfering_foci_count}</div>
                <div class="soc-intel-stat__lbl">Críticos</div>
            </div>
            <div class="soc-intel-stat">
                <div class="soc-intel-stat__val">{result.monitored_foci_count}</div>
                <div class="soc-intel-stat__lbl">Monitorados</div>
            </div>
            <div class="soc-intel-stat">
                <div class="soc-intel-stat__val">{radius_km}</div>
                <div class="soc-intel-stat__lbl">Raio km</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="soc-intel-section">Resumo do trajeto</div>', unsafe_allow_html=True)
    route_label = "Desvio validado" if result.has_detour else "Rota principal"
    st.markdown(
        f"""
        <div class="soc-route-summary">
            <div><span>Trajeto ativo</span><strong>{route_label}</strong></div>
            <div><span>Distância original</span><strong>{result.route_distance_km:.1f} km</strong></div>
            <div><span>Distância validada</span><strong>{result.display_distance:.1f} km</strong></div>
            <div><span>Waypoints</span><strong>{len(result.validated_route)}</strong></div>
            <div><span>Taxa de desvio</span><strong>{mission.diversion_rate:.1f}%</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not result.interfering_foci:
        st.markdown(
            '<div class="soc-intel-empty">✅ Nenhuma ameaça crítica na rota operacional.</div>',
            unsafe_allow_html=True,
        )
        return

    st.markdown('<div class="soc-intel-section">Ameaças ativas</div>', unsafe_allow_html=True)
    for hotspot in result.interfering_foci:
        severity = hotspot.get("severity", "—")
        st.markdown(
            f"""
            <div class="hotspot-item hotspot-item--critical">
                <div class="hotspot-item__header">
                    <strong>{hotspot.get('description', 'Foco de incêndio')}</strong>
                    {_severity_badge(str(severity))}
                </div>
                <div class="hotspot-item__metrics">
                    <span>📏 {hotspot['distance_km']:.2f} km</span>
                    <span>⭕ {hotspot.get('effective_radius_km', radius_km):.2f} km</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if result.monitored_foci_count > result.interfering_foci_count:
        st.markdown('<div class="soc-intel-section">Focos em observação</div>', unsafe_allow_html=True)
        blocking_ids = {h.get("id") for h in result.interfering_foci}
        for hotspot in result.monitored_foci:
            if hotspot.get("id") in blocking_ids:
                continue
            st.markdown(
                f"""
                <div class="hotspot-item">
                    <div class="hotspot-item__header">
                        <strong>{hotspot.get('description', 'Foco')}</strong>
                        {_severity_badge(str(hotspot.get('severity', '—')))}
                    </div>
                    <div class="hotspot-item__metrics">
                        <span>📏 {hotspot.get('distance_km', 0):.2f} km</span>
                        <span>Monitorado</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
