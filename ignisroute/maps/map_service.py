from pathlib import Path
from typing import Any

import folium
from folium import plugins

Route = list[tuple[float, float]]
Hotspot = dict[str, Any]


# ==========================================================
# Configurações Visuais
# ==========================================================

COLORS = {
    "safe_route": "#22c55e",
    "blocked_route": "#ef4444",
    "detour_route": "#3b82f6",
    "danger_zone": "#f97316",
    "monitor_zone": "#fb923c",
}


# ==========================================================
# Helpers
# ==========================================================

def _get_map_center(route: Route) -> tuple[float, float]:
    return (
        sum(lat for lat, _ in route) / len(route),
        sum(lon for _, lon in route) / len(route),
    )


def _create_base_map(route: Route) -> folium.Map:
    center = _get_map_center(route)

    map_object = folium.Map(
        location=center,
        zoom_start=12,
        control_scale=True,
        tiles="CartoDB dark_matter",
        attr=" ",
    )

    map_object.options["attributionControl"] = False

    return map_object


# ==========================================================
# Legenda
# ==========================================================

def _add_legend(map_object: folium.Map) -> None:

    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index:9999;
        background: rgba(15,23,42,.92);
        color:white;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(255,255,255,.1);
        font-size:13px;
        line-height:1.8;
        box-shadow:0 8px 24px rgba(0,0,0,.35);
    ">
        <b>IGNISROUTE</b><br>
        🟩 Rota Validada<br>
        🟥 Rota Bloqueada<br>
        🟦 Rota de Desvio<br>
        🟧 Zona de Exclusão<br>
        🔥 Foco de Calor
    </div>
    """

    map_object.get_root().html.add_child(
        folium.Element(legend_html)
    )


# ==========================================================
# Rotas
# ==========================================================

def _add_route_markers(
    layer: folium.FeatureGroup,
    route: Route,
) -> None:

    folium.Marker(
        route[0],
        tooltip="Origem",
        icon=folium.Icon(
            color="green",
            icon="play",
            prefix="fa",
        ),
    ).add_to(layer)

    folium.Marker(
        route[-1],
        tooltip="Destino",
        icon=folium.Icon(
            color="red",
            icon="flag",
            prefix="fa",
        ),
    ).add_to(layer)


def _draw_original_route(
    layer: folium.FeatureGroup,
    route: Route,
) -> None:

    folium.PolyLine(
        route,
        color=COLORS["blocked_route"],
        weight=5,
        opacity=0.55,
        dash_array="6 8",
        tooltip="Rota original bloqueada",
    ).add_to(layer)


def _draw_detour_route(
    layer: folium.FeatureGroup,
    route: Route,
) -> None:

    folium.PolyLine(
        route,
        color=COLORS["detour_route"],
        weight=4,
        opacity=0.75,
        dash_array="10 6",
        tooltip="Rota alternativa",
    ).add_to(layer)


def _draw_validated_route(
    layer: folium.FeatureGroup,
    route: Route,
) -> None:

    folium.PolyLine(
        route,
        color=COLORS["safe_route"],
        weight=7,
        opacity=0.9,
        tooltip="Rota validada",
    ).add_to(layer)


# ==========================================================
# Hotspots
# ==========================================================

def _create_hotspot_popup(
    hotspot: Hotspot,
    is_blocking: bool,
) -> str:

    distance = hotspot.get("distance_km")

    return f"""
    <b>{hotspot.get('description', 'Foco')}</b><br>
    Severidade: {hotspot.get('severity', 'N/A')}<br>
    Distância: {distance:.2f} km<br>
    {'⚠️ INTERFERINDO NA ROTA' if is_blocking else 'Monitorado'}
    """


def _add_hotspots(
    map_layer: folium.FeatureGroup,
    zone_layer: folium.FeatureGroup,
    hotspots: list[Hotspot],
    blocked_ids: set,
    radius_km: float,
) -> None:

    for hotspot in hotspots:

        location = (
            hotspot["latitude"],
            hotspot["longitude"],
        )

        is_blocking = hotspot.get("id") in blocked_ids

        zone_color = (
            COLORS["danger_zone"]
            if is_blocking
            else COLORS["monitor_zone"]
        )

        folium.Circle(
            location=location,
            radius=radius_km * 1000,
            color=zone_color,
            fill=True,
            fill_color=zone_color,
            fill_opacity=0.18 if is_blocking else 0.10,
            weight=2 if is_blocking else 1,
        ).add_to(zone_layer)

        folium.Marker(
            location=location,
            tooltip=hotspot.get(
                "description",
                "Foco de calor",
            ),
            popup=folium.Popup(
                _create_hotspot_popup(
                    hotspot,
                    is_blocking,
                ),
                max_width=260,
            ),
            icon=folium.Icon(
                color="darkred" if is_blocking else "orange",
                icon="fire",
                prefix="fa",
            ),
        ).add_to(map_layer)


# ==========================================================
# Plugins
# ==========================================================

def _add_plugins(map_object: folium.Map) -> None:

    plugins.Fullscreen(
        position="topright"
    ).add_to(map_object)


# ==========================================================
# Public API
# ==========================================================

def build_route_map(
    route: Route,
    hotspots: list[Hotspot],
    radius_km: float,
    alt_route: Route | None = None,
    blocked: bool = False,
    validated_route: Route | None = None,
    blocked_hotspots: list[Hotspot] | None = None,
) -> folium.Map:

    map_object = _create_base_map(route)

    blocked_ids = {
        hotspot.get("id")
        for hotspot in (blocked_hotspots or [])
    }

    route_layer = folium.FeatureGroup(
        name="Rotas",
        show=True,
    )

    hotspot_layer = folium.FeatureGroup(
        name="Focos",
        show=True,
    )

    zone_layer = folium.FeatureGroup(
        name="Zonas de Risco",
        show=True,
    )

    _add_route_markers(
        route_layer,
        route,
    )

    if blocked:
        _draw_original_route(
            route_layer,
            route,
        )

    if blocked and alt_route:
        _draw_detour_route(
            route_layer,
            alt_route,
        )

    display_route = (
        validated_route
        or alt_route
        or route
    )

    _draw_validated_route(
        route_layer,
        display_route,
    )

    _add_hotspots(
        hotspot_layer,
        zone_layer,
        hotspots,
        blocked_ids,
        radius_km,
    )

    route_layer.add_to(map_object)
    hotspot_layer.add_to(map_object)
    zone_layer.add_to(map_object)

    _add_plugins(map_object)
    _add_legend(map_object)

    return map_object


def export_map_html(
    map_object: folium.Map,
    path: str,
) -> str:

    output = Path(path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    map_object.save(
        str(output)
    )

    return str(output)