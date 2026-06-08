import streamlit as st

from models.route_result import RouteAnalysisResult
from services.analytics_service import focos_dataframe, sensor_distribution, severity_distribution


def render_operational_intel(result: RouteAnalysisResult) -> None:
    st.markdown(
        """
        <div class="soc-section-head">
            <p class="section-title section-title--inline">Panorama analítico do cenário</p>
            <span class="soc-section-head__hint">Dados operacionais em tempo real</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    source_label = {
        "postgresql": "vw_focos_incendio · PostgreSQL",
        "supabase": "vw_focos_incendio · Supabase REST",
        "fallback": "Dataset local de contingência",
    }.get(result.data_source, result.data_source)

    st.markdown(
        f"""
        <div class="soc-analytics-source">
            Fonte: <strong>{source_label}</strong>
            {" · Base conectada" if result.database_connected else " · Sem conexão com a base"}
        </div>
        """,
        unsafe_allow_html=True,
    )

    foci = result.monitored_foci
    if not foci:
        st.info(
            "Nenhum foco ativo no cenário. Ative **Alerta de Queimada** para carregar "
            "os registros analíticos do banco de dados."
        )
        return

    chart_col, sensor_col = st.columns(2, gap="medium")

    with chart_col:
        st.markdown('<div class="soc-chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="soc-intel-section">Distribuição por severidade</div>', unsafe_allow_html=True)
        st.bar_chart(severity_distribution(foci), height=240)
        st.markdown("</div>", unsafe_allow_html=True)

    with sensor_col:
        st.markdown('<div class="soc-chart-panel">', unsafe_allow_html=True)
        st.markdown('<div class="soc-intel-section">Detecções por sensor</div>', unsafe_allow_html=True)
        st.bar_chart(sensor_distribution(foci), height=240)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="soc-intel-section">Focos monitorados — registros da view</div>', unsafe_allow_html=True)
    st.dataframe(
        focos_dataframe(foci),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Distância à rota (km)": st.column_config.NumberColumn(format="%.2f"),
            "Raio afetado (m)": st.column_config.NumberColumn(format="%.0f"),
        },
    )
