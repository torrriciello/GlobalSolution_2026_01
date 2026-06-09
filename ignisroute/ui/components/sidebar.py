from dataclasses import dataclass

import streamlit as st

from services.location_repository import LocationLoadResult, find_location, load_locations
from ui.constants import SCENARIOS


@dataclass
class OperationParams:
    scenario: str
    radius_km: float
    origin_label: str
    destination_label: str
    origin_lat: float | None
    origin_lon: float | None
    destination_lat: float | None
    destination_lon: float | None
    region_label: str
    locations_source: str
    locations_connected: bool
    ready: bool


@st.cache_data(ttl=600, show_spinner=False)
def _cached_locations() -> LocationLoadResult:
    return load_locations()


def render_sidebar() -> OperationParams:
    location_load = _cached_locations()
    locations = location_load.locations
    location_names = [loc.name for loc in locations]

    with st.sidebar:
        st.markdown(
            """
            <div class="soc-sidebar-header">
                <div class="soc-sidebar-header__icon">⚙️</div>
                <div>
                    <div class="soc-sidebar-header__title">Painel de Controle</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not location_load.connected:
            st.error("Conexão com PostgreSQL necessária para carregar localidades.")
            return OperationParams(
                scenario=SCENARIOS[0],
                radius_km=5.0,
                origin_label="—",
                destination_label="—",
                origin_lat=None,
                origin_lon=None,
                destination_lat=None,
                destination_lon=None,
                region_label="Base indisponível",
                locations_source=location_load.source,
                locations_connected=False,
                ready=False,
            )

        source_label = {
            "postgresql": "PostgreSQL",
            "supabase": "Supabase REST",
        }.get(location_load.source, location_load.source)

        st.markdown('<div class="soc-sidebar-section">Planejamento de missão</div>', unsafe_allow_html=True)

        if len(locations) < 2:
            st.error("A base precisa de ao menos duas localidades geográficas.")
            return OperationParams(
                scenario=SCENARIOS[0],
                radius_km=5.0,
                origin_label="—",
                destination_label="—",
                origin_lat=None,
                origin_lon=None,
                destination_lat=None,
                destination_lon=None,
                region_label=location_load.region_label,
                locations_source=location_load.source,
                locations_connected=location_load.connected,
                ready=False,
            )

        origin_label = st.selectbox(
            "Origem",
            location_names,
            index=0,
            help="dim_municipio + dim_regiao_geografica",
        )

        dest_options = [name for name in location_names if name != origin_label]
        default_dest_index = 1 if len(dest_options) > 1 else 0
        destination_label = st.selectbox(
            "Destino",
            dest_options,
            index=default_dest_index,
            help="dim_municipio + dim_regiao_geografica",
        )

        origin = find_location(locations, origin_label)
        destination = find_location(locations, destination_label)
        region_label = location_load.region_label

        if origin and destination:
            states = sorted({origin.uf, destination.uf})
            region_label = f"{origin.municipality} → {destination.municipality} · {', '.join(states)}"

        st.markdown('<div class="soc-sidebar-section">Modo de análise</div>', unsafe_allow_html=True)
        scenario = st.selectbox(
            "Modo",
            SCENARIOS,
            index=1,
            label_visibility="collapsed",
            help="Alerta de Queimada consulta vw_focos_ativos em tempo real.",
        )

        st.markdown('<div class="soc-sidebar-section">Margem de segurança</div>', unsafe_allow_html=True)
        radius_km = st.slider(
            "Raio de exclusão (km)",
            min_value=1,
            max_value=15,
            value=5,
            step=1,
            label_visibility="collapsed",
        )

        st.markdown(
            f'<div class="soc-radius-display">Margem ativa: <strong>{radius_km} km</strong></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

    return OperationParams(
        scenario=scenario,
        radius_km=radius_km,
        origin_label=origin_label,
        destination_label=destination_label,
        origin_lat=origin.lat if origin else None,
        origin_lon=origin.lon if origin else None,
        destination_lat=destination.lat if destination else None,
        destination_lon=destination.lon if destination else None,
        region_label=region_label,
        locations_source=location_load.source,
        locations_connected=location_load.connected,
        ready=bool(origin and destination),
    )
