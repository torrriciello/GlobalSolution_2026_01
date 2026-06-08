from dataclasses import dataclass

import streamlit as st

from models.route_result import Route
from services.location_repository import LocationLoadResult, find_location, load_locations
from services.route_builder import build_mission_route
from services.routing_service import RoutedPath
from ui.constants import SCENARIOS


@dataclass
class OperationParams:
    scenario: str
    radius_km: float
    origin_label: str
    destination_label: str
    main_route: Route | None
    routed_path: RoutedPath | None
    region_label: str
    locations_source: str
    locations_connected: bool


@st.cache_data(ttl=600, show_spinner=False)
def _cached_locations() -> LocationLoadResult:
    return load_locations()


@st.cache_data(ttl=1800, show_spinner="Calculando rota viária...")
def _cached_road_route(
    origin_lat: float,
    origin_lon: float,
    dest_lat: float,
    dest_lon: float,
) -> RoutedPath:
    return build_mission_route((origin_lat, origin_lon), (dest_lat, dest_lon))


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
                    <div class="soc-sidebar-header__sub">Dados reais · roteamento viário</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        source_label = {
            "postgresql": "PostgreSQL",
            "supabase": "Supabase REST",
            "fallback": "Modo demonstração",
        }.get(location_load.source, location_load.source)
        status_class = "soc-sidebar-db--online" if location_load.connected else "soc-sidebar-db--offline"

        st.markdown('<div class="soc-sidebar-section">Planejamento de missão</div>', unsafe_allow_html=True)

        if len(locations) < 2:
            st.error("É necessário ao menos duas localidades no banco para planejar a rota.")
            return OperationParams(
                scenario=SCENARIOS[0],
                radius_km=5.0,
                origin_label="—",
                destination_label="—",
                main_route=None,
                routed_path=None,
                region_label=location_load.region_label,
                locations_source=location_load.source,
                locations_connected=location_load.connected,
            )

        origin_label = st.selectbox(
            "Origem",
            location_names,
            index=0,
            help="Município carregado de dim_municipio e dim_regiao_geografica.",
        )

        dest_options = [name for name in location_names if name != origin_label]
        default_dest_index = 1 if len(dest_options) > 1 else 0
        destination_label = st.selectbox(
            "Destino",
            dest_options,
            index=default_dest_index,
            help="Destino operacional registrado na base geográfica.",
        )

        origin = find_location(locations, origin_label)
        destination = find_location(locations, destination_label)
        main_route = None
        routed_path = None
        region_label = location_load.region_label

        if origin and destination:
            routed_path = _cached_road_route(origin.lat, origin.lon, destination.lat, destination.lon)
            main_route = routed_path.geometry
            states = sorted({origin.uf, destination.uf})
            region_label = f"{origin.municipality} → {destination.municipality} · {', '.join(states)}"

            routing_label = "Malha viária OSRM" if routed_path.source == "osrm" else "Trajeto estimado"
            st.markdown(
                f"""
                <div class="soc-route-preview">
                    <div><span>Roteamento</span><strong>{routing_label}</strong></div>
                    <div><span>Distância</span><strong>{routed_path.distance_km:.1f} km</strong></div>
                    <div><span>Tempo estimado</span><strong>{routed_path.duration_min:.0f} min</strong></div>
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
            help="Alerta de Queimada carrega focos ativos de vw_focos_incendio.",
        )

        st.markdown('<div class="soc-sidebar-section">Margem de segurança</div>', unsafe_allow_html=True)
        radius_km = st.slider(
            "Raio de exclusão (km)",
            min_value=1,
            max_value=15,
            value=5,
            step=1,
            label_visibility="collapsed",
            help="Distância mínima entre a rota viária e cada foco ativo.",
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
        main_route=main_route,
        routed_path=routed_path,
        region_label=region_label,
        locations_source=location_load.source,
        locations_connected=location_load.connected,
    )
