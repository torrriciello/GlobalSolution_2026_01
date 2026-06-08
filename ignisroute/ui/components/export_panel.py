from pathlib import Path

import streamlit as st

from models.route_result import RouteAnalysisResult


def render_export_panel(result: RouteAnalysisResult, json_path: str) -> None:
    st.markdown('<div class="soc-intel-section">Exportação</div>', unsafe_allow_html=True)

    if result.map_html_path and Path(result.map_html_path).exists():
        with open(result.map_html_path, "rb") as html_file:
            st.download_button(
                label="⬇ Mapa tático HTML",
                data=html_file,
                file_name="rota_tatica.html",
                mime="text/html",
                use_container_width=True,
                key="dl_html",
            )

    if Path(json_path).exists():
        with open(json_path, "r", encoding="utf-8") as json_file:
            st.download_button(
                label="⬇ Relatório JSON",
                data=json_file.read(),
                file_name="analise_rota.json",
                mime="application/json",
                use_container_width=True,
                key="dl_json",
            )
