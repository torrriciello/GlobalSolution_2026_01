import streamlit as st

from models.route_result import RouteAnalysisResult
from services.analytics_service import OperationalMetrics


def _metric_card(label: str, value: str, sub: str, css_class: str) -> str:
    return f"""
    <div class="soc-kpi">
        <div class="soc-kpi__label">{label}</div>
        <div class="soc-kpi__value {css_class}">{value}</div>
        <div class="soc-kpi__sub">{sub}</div>
    </div>
    """


def _severity_css(severity: str) -> str:
    key = severity.lower()
    if key in {"crítico", "critico"}:
        return "status-interditada"
    if key == "alto":
        return "status-warn"
    if key in {"médio", "medio"}:
        return "status-info"
    return "status-livre"


def render_kpi_dashboard(result: RouteAnalysisResult, metrics: OperationalMetrics) -> None:
    st.markdown(
        """
        <div class="soc-section-head">
            <p class="section-title section-title--inline">Indicadores operacionais</p>
            <span class="soc-section-head__hint">Métricas derivadas de vw_focos_ativos</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns(6)
    kpi_data = [
        ("Status da via", result.status_label, "Resultado da validação", result.status_css),
        ("Focos críticos", str(metrics.interfering_count), "Interferindo na rota", "status-warn"),
        ("Focos ativos", str(metrics.active_foci), "Status ATIVO na view", "status-warn"),
        ("Sensores operantes", str(metrics.active_sensors), "Fontes de detecção ativas", "status-info"),
        ("Severidade máxima", metrics.max_severity, "Maior nível detectado", _severity_css(metrics.max_severity)),
        ("Distância média", f"{metrics.avg_distance_km:.1f} km", "Foco → rota planejada", "status-info"),
    ]

    for col, (label, value, sub, css) in zip(cols, kpi_data):
        with col:
            st.markdown(_metric_card(label, value, sub, css), unsafe_allow_html=True)
