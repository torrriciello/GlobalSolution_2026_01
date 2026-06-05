import streamlit as st
from streamlit_folium import st_folium

from maps.map_service import build_route_map
from services.supabase_service import get_hotspots
from services.risk_service import (
    create_detour_route,
    find_risky_hotspots,
    get_route_distance_km,
)

MAIN_ROUTE = [
    (-23.5048, -46.6299),  # Saída: Santana (zona norte)
    (-23.5505, -46.6333),  # Intermediário: Centro
    (-23.5934, -46.6305),  # Destino: Vila Mariana (zona sul)
]


def main():
    st.set_page_config(page_title="IgnisRoute", page_icon="🔥", layout="wide")
    st.title("🔥 IgnisRoute — Sistema Tático de Navegação")
    st.markdown(
        "Sistema desenvolvido para apoiar ações de Defesa Civil e Corpo de Bombeiros na tomada de decisão durante ocorrências de incêndios florestais."
    )

    st.sidebar.header("Cenários")
    scenario = st.sidebar.selectbox(
        "Escolha um cenário",
        ["Via Livre", "Alerta de Queimada"],
        index=0,
        help="Via Livre mantém a rota principal; Alerta de Queimada ativa a avaliação de risco e desvio automático.",
    )
    radius_km = st.sidebar.slider("Raio de segurança (km)", min_value=1, max_value=15, value=5, step=1)
    show_details = st.sidebar.checkbox("Mostrar detalhes do hotspot", value=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "### Instruções\n\n1. Carregue o projeto em um ambiente com `Streamlit` e `python-dotenv`.\n2. Configure `.env` com `SUPABASE_URL` e `SUPABASE_KEY`.\n3. Execute `streamlit run app.py`."
    )

    hotspots, connected = get_hotspots()
    if scenario == "Via Livre":
        hotspots = []

    blocked_hotspots = find_risky_hotspots(MAIN_ROUTE, hotspots, radius_km)
    blocked = len(blocked_hotspots) > 0
    alt_route = create_detour_route(MAIN_ROUTE) if blocked else None

    status_label = "Livre" if not blocked else "Bloqueada"
    alert_color = "success" if not blocked else "error"

    st.markdown("---")
    st.subheader("Resumo da Rota")
    st.metric("Status da rota", status_label)
    st.metric("Hotspots avaliados", len(hotspots))
    st.metric("Distância total da rota", f"{get_route_distance_km(MAIN_ROUTE):.1f} km")

    if blocked:
        st.warning(
            f"A rota principal foi bloqueada pelo menos por um hotspot dentro do raio de {radius_km} km. Uma rota alternativa foi gerada automaticamente."
        )
    else:
        st.success("Rota livre de riscos dentro do raio de segurança definido.")

    if connected:
        st.info("Conexão com Supabase estabelecida com sucesso.")
    else:
        st.info("Usando dados de fallback local. Verifique as credenciais do Supabase se desejar conexão real.")

    map_object = build_route_map(MAIN_ROUTE, hotspots, radius_km, alt_route=alt_route, blocked=blocked)
    st_data = st_folium(map_object, width=1100, height=700)

    if show_details:
        with st.expander("Detalhes da simulação e hotspots"):
            if not hotspots:
                st.write("Nenhum hotspot ativo foi avaliado neste cenário.")
            else:
                st.write(f"Hotspots dentro do raio de {radius_km} km:")
                for hotspot in blocked_hotspots:
                    st.write(
                        f"- **{hotspot.get('description', 'Foco de incêndio')}**: distância {hotspot['distance_km']:.2f} km, severidade {hotspot.get('severity', 'Desconhecida')}"
                    )
            if blocked and alt_route:
                detour_distance = get_route_distance_km(alt_route)
                st.write(f"**Rota alternativa:** {detour_distance:.1f} km")

    st.markdown("---")
    st.markdown(
        "IgnisRoute MVP v1.0 — sistema de navegação tática para cenários de incêndio florestal."
    )


if __name__ == "__main__":
    main()
