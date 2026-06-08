from pathlib import Path
from typing import Any

import folium
from folium import plugins

Route = list[tuple[float, float]]
Hotspot = dict[str, Any]

COLORS = {
    "safe_route": "#34d399",
    "safe_glow": "#065f46",
    "blocked_route": "#f87171",
    "detour_route": "#60a5fa",
    "detour_glow": "#1e3a8a",
    "danger_zone": "#fb923c",
    "origin": "#22c55e",
    "destination": "#ef4444",
}

MAP_STYLES = """
<style>
    .ignis-route-marker {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        font-weight: 800;
        font-size: 11px;
        letter-spacing: 0.5px;
        color: #fff;
        border: 2px solid rgba(255,255,255,0.9);
        box-shadow: 0 8px 24px rgba(0,0,0,0.45);
    }
    .ignis-route-marker--origin { background: linear-gradient(135deg, #22c55e, #15803d); }
    .ignis-route-marker--dest { background: linear-gradient(135deg, #ef4444, #991b1b); }
    .ignis-hotspot-marker {
        width: 14px;
        height: 14px;
        border-radius: 50%;
        border: 2px solid #fff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.35);
    }
    .ignis-hotspot-marker--critical { background: #ef4444; }
    .ignis-hotspot-marker--monitor { background: #f59e0b; }
</style>
"""


def _get_bounds(routes: list[Route], hotspots: list[Hotspot]) -> list[list[float]]:
    points: list[tuple[float, float]] = []
    for route in routes:
        points.extend(route)
    for hotspot in hotspots:
        points.append((hotspot["latitude"], hotspot["longitude"]))

    if not points:
        return [[-23.55, -46.63], [-23.56, -46.64]]

    lats = [lat for lat, _ in points]
    lons = [lon for _, lon in points]
    return [[min(lats), min(lons)], [max(lats), max(lons)]]


def _create_base_map(bounds: list[list[float]]) -> folium.Map:
    center_lat = (bounds[0][0] + bounds[1][0]) / 2
    center_lon = (bounds[0][1] + bounds[1][1]) / 2

    map_object = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        control_scale=True,
        tiles="CartoDB dark_matter",
        attr=" ",
    )
    map_object.options["attributionControl"] = False
    map_object.fit_bounds(bounds, padding=(50, 50))
    map_object.get_root().html.add_child(folium.Element(MAP_STYLES))
    return map_object


def _add_legend(map_object: folium.Map, routing_source: str) -> None:
    engine = "Malha viária OSRM" if routing_source == "osrm" else "Trajeto estimado"
    legend_html = f"""
    <div style="
        position: fixed;
        bottom: 28px;
        left: 28px;
        z-index:9999;
        background: rgba(2,6,23,.92);
        color:#f8fafc;
        padding:14px 16px;
        border-radius:14px;
        border:1px solid rgba(255,255,255,.12);
        font-size:12px;
        line-height:1.7;
        box-shadow:0 12px 32px rgba(0,0,0,.4);
        backdrop-filter:blur(12px);
        font-family: Inter, sans-serif;
    ">
        <div style="font-weight:800;font-size:13px;margin-bottom:6px;letter-spacing:.5px;">IGNISROUTE</div>
        <div style="color:#94a3b8;font-size:11px;margin-bottom:8px;">{engine}</div>
        <div><span style="color:#34d399;font-weight:700;">━━</span> Rota validada</div>
        <div><span style="color:#f87171;font-weight:700;">╌╌</span> Rota bloqueada</div>
        <div><span style="color:#60a5fa;font-weight:700;">━━</span> Desvio operacional</div>
        <div><span style="color:#f59e0b;">●</span> Foco monitorado</div>
        <div><span style="color:#ef4444;">●</span> Foco crítico</div>
    </div>
    """
    map_object.get_root().html.add_child(folium.Element(legend_html))


def _draw_route_line(
    layer: folium.FeatureGroup,
    route: Route,
    color: str,
    glow_color: str,
    weight: int = 7,
    opacity: float = 0.95,
    dash_array: str | None = None,
    tooltip: str = "Rota",
) -> None:
    folium.PolyLine(
        route,
        color=glow_color,
        weight=weight + 5,
        opacity=0.28,
        tooltip=tooltip,
    ).add_to(layer)

    folium.PolyLine(
        route,
        color=color,
        weight=weight,
        opacity=opacity,
        dash_array=dash_array,
        tooltip=tooltip,
    ).add_to(layer)


def _add_route_markers(
    layer: folium.FeatureGroup,
    route: Route,
    origin_label: str = "Origem",
    destination_label: str = "Destino",
) -> None:
    folium.Marker(
        route[0],
        tooltip=origin_label,
        icon=folium.DivIcon(
            html='<div class="ignis-route-marker ignis-route-marker--origin">O</div>',
            icon_size=(34, 34),
            icon_anchor=(17, 17),
        ),
    ).add_to(layer)

    folium.Marker(
        route[-1],
        tooltip=destination_label,
        icon=folium.DivIcon(
            html='<div class="ignis-route-marker ignis-route-marker--dest">D</div>',
            icon_size=(34, 34),
            icon_anchor=(17, 17),
        ),
    ).add_to(layer)


def _create_hotspot_popup(hotspot: Hotspot, is_blocking: bool) -> str:
    distance = hotspot.get("distance_km", 0)
    status = "Interferindo na rota" if is_blocking else "Em observação"
    return f"""
    <div style="font-family:Inter,sans-serif;min-width:180px;">
        <b>{hotspot.get('description', 'Foco')}</b><br>
        Severidade: {hotspot.get('severity', 'N/A')}<br>
        Sensor: {hotspot.get('sensor', '—')}<br>
        Distância à rota: {distance:.2f} km<br>
        <span style="color:{'#ef4444' if is_blocking else '#f59e0b'};">{status}</span>
    </div>
    """


def _add_hotspots(
    map_layer: folium.FeatureGroup,
    zone_layer: folium.FeatureGroup,
    hotspots: list[Hotspot],
    blocked_ids: set,
) -> None:
    for hotspot in hotspots:
        location = (hotspot["latitude"], hotspot["longitude"])
        is_blocking = hotspot.get("id") in blocked_ids
        marker_class = "ignis-hotspot-marker--critical" if is_blocking else "ignis-hotspot-marker--monitor"

        if is_blocking:
            zone_radius_m = float(hotspot.get("effective_radius_km", 5)) * 1000
            folium.Circle(
                location=location,
                radius=zone_radius_m,
                color=COLORS["danger_zone"],
                fill=True,
                fill_color=COLORS["danger_zone"],
                fill_opacity=0.05,
                weight=1,
                opacity=0.35,
                dash_array="6 8",
            ).add_to(zone_layer)

        folium.Marker(
            location=location,
            tooltip=hotspot.get("description", "Foco de calor"),
            popup=folium.Popup(
                _create_hotspot_popup(hotspot, is_blocking),
                max_width=280,
            ),
            icon=folium.DivIcon(
                html=f'<div class="ignis-hotspot-marker {marker_class}"></div>',
                icon_size=(14, 14),
                icon_anchor=(7, 7),
            ),
        ).add_to(map_layer)


def build_route_map(
    route: Route,
    hotspots: list[Hotspot],
    radius_km: float,
    alt_route: Route | None = None,
    blocked: bool = False,
    validated_route: Route | None = None,
    blocked_hotspots: list[Hotspot] | None = None,
    origin_label: str = "Origem",
    destination_label: str = "Destino",
    routing_source: str = "osrm",
) -> folium.Map:
    blocked_ids = {hotspot.get("id") for hotspot in (blocked_hotspots or [])}
    display_route = validated_route or alt_route or route

    routes_for_bounds = [route, display_route]
    if alt_route:
        routes_for_bounds.append(alt_route)

    map_object = _create_base_map(_get_bounds(routes_for_bounds, hotspots))

    route_layer = folium.FeatureGroup(name="Trajeto operacional", show=True)
    hotspot_layer = folium.FeatureGroup(name="Focos ativos", show=True)
    zone_layer = folium.FeatureGroup(name="Zonas críticas", show=False)

    _add_route_markers(route_layer, display_route, origin_label, destination_label)

    if blocked and route != display_route:
        _draw_route_line(
            route_layer,
            route,
            COLORS["blocked_route"],
            "#7f1d1d",
            weight=4,
            opacity=0.45,
            dash_array="8 10",
            tooltip="Rota original bloqueada",
        )

    if blocked and alt_route and alt_route != display_route:
        _draw_route_line(
            route_layer,
            alt_route,
            COLORS["detour_route"],
            COLORS["detour_glow"],
            weight=5,
            opacity=0.65,
            tooltip="Desvio calculado",
        )

    _draw_route_line(
        route_layer,
        display_route,
        COLORS["safe_route"],
        COLORS["safe_glow"],
        weight=8,
        opacity=1.0,
        tooltip="Rota validada",
    )

    _add_hotspots(hotspot_layer, zone_layer, hotspots, blocked_ids)

    route_layer.add_to(map_object)
    hotspot_layer.add_to(map_object)
    zone_layer.add_to(map_object)

    folium.LayerControl(collapsed=True).add_to(map_object)
    plugins.Fullscreen(position="topright").add_to(map_object)
    _add_legend(map_object, routing_source)

    return map_object


def export_map_html(map_object: folium.Map, path: str) -> str:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    map_object.save(str(output))
    return str(output)
