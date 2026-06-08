import streamlit as st

from models.route_result import RouteAnalysisResult


def _severity_badge(severity: str) -> str:
    key = str(severity).lower().strip()
    css = {
        "crítico": "critical",
        "critico": "critical",
        "alto": "high",
        "médio": "medium",
        "medio": "medium",
        "baixo": "low",
    }.get(key, "medium")
    return f'<span class="soc-severity soc-severity--{css}">{severity}</span>'


def _route_extra_pct(result: RouteAnalysisResult) -> float:
    if not result.detour_distance_km or not result.route_distance_km:
        return 0.0
    extra = result.detour_distance_km - result.route_distance_km
    return round((extra / result.route_distance_km) * 100, 1)


def render_threat_intel(result: RouteAnalysisResult, radius_km: float) -> None:
    st.markdown(
        """
        <div class="soc-panel-header">
            <span class="soc-panel-header__title">Riscos e trajeto validado</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    route_label = "Desvio validado" if result.has_detour else "Rota viária validada"
    routing_label = "Malha viária OSRM" if result.routing_source == "osrm" else "Trajeto estimado"
    duration = result.detour_duration_min if result.has_detour and result.detour_duration_min else result.route_duration_min
    extra_km = 0.0
    if result.detour_distance_km:
        extra_km = max(result.detour_distance_km - result.route_distance_km, 0)

    st.markdown(
        f"""
        <div class="soc-route-summary soc-route-summary--highlight">
            <div><span>Trajeto ativo</span><strong>{route_label}</strong></div>
            <div><span>Motor de rota</span><strong>{routing_label}</strong></div>
            <div><span>Distância validada</span><strong>{result.display_distance:.1f} km</strong></div>
            <div><span>Tempo estimado</span><strong>{duration:.0f} min</strong></div>
            <div><span>Focos críticos</span><strong>{result.interfering_foci_count}</strong></div>
            <div><span>Focos monitorados</span><strong>{result.monitored_foci_count}</strong></div>
            <div><span>Acréscimo de rota</span><strong>{"+" + f"{extra_km:.1f}" + " km (" + f"{_route_extra_pct(result):.0f}" + "%)" if extra_km > 0 else "—"}</strong></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not result.interfering_foci:
        st.markdown(
            '<div class="soc-intel-empty">Nenhum foco crítico interfere na rota dentro da margem configurada.</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown('<div class="soc-intel-section">Focos críticos na rota</div>', unsafe_allow_html=True)
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
                        <span>📏 {hotspot['distance_km']:.2f} km da rota</span>
                        <span>⭕ {hotspot.get('effective_radius_km', radius_km):.2f} km</span>
                        <span>🛰️ {hotspot.get('sensor', '—')}</span>
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
                        <span>🛰️ {hotspot.get('sensor', '—')}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
