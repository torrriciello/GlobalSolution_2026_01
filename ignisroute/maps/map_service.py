from pathlib import Path
from typing import Any

import folium
from folium import plugins

from utils.haversine import closest_point_on_route

Route = list[tuple[float, float]]
Hotspot = dict[str, Any]

COLORS = {
    "safe_route": "#34d399",
    "safe_glow": "#065f46",
    "blocked_route": "#f87171",
    "detour_route": "#60a5fa",
    "detour_glow": "#1e3a8a",
    "danger_zone": "#fb923c",
    "impact_line": "#f87171",
}


MAP_STYLES = """
<style>
    @keyframes ignis-pulse-critical {
        0% { box-shadow: 0 0 0 0 rgba(239,68,68,.65); transform: scale(1); }
        70% { box-shadow: 0 0 0 14px rgba(239,68,68,0); transform: scale(1.08); }
        100% { box-shadow: 0 0 0 0 rgba(239,68,68,0); transform: scale(1); }
    }
    @keyframes ignis-pulse-monitor {
        0% { box-shadow: 0 0 0 0 rgba(245,158,11,.45); }
        70% { box-shadow: 0 0 0 10px rgba(245,158,11,0); }
        100% { box-shadow: 0 0 0 0 rgba(245,158,11,0); }
    }
    .ignis-route-marker {
        display: flex; align-items: center; justify-content: center;
        width: 38px; height: 38px; border-radius: 50%;
        font-weight: 800; font-size: 12px; color: #fff;
        border: 2px solid rgba(255,255,255,0.95);
        box-shadow: 0 10px 28px rgba(0,0,0,0.5);
    }
    .ignis-route-marker--origin { background: linear-gradient(135deg, #22c55e, #15803d); }
    .ignis-route-marker--dest { background: linear-gradient(135deg, #ef4444, #991b1b); }
    .ignis-hotspot-marker {
        width: 16px; height: 16px; border-radius: 50%;
        border: 2px solid #fff;
    }
    .ignis-hotspot-marker--critical {
        background: #ef4444;
        animation: ignis-pulse-critical 2s ease-out infinite;
    }
    .ignis-hotspot-marker--monitor {
        background: #f59e0b;
        animation: ignis-pulse-monitor 3s ease-out infinite;
    }
    .ignis-impact-point {
        width: 10px; height: 10px; border-radius: 50%;
        background: #ef4444; border: 2px solid #fff;
        box-shadow: 0 0 12px rgba(239,68,68,.8);
    }
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
    map_object.fit_bounds(bounds, padding=(60, 60))
    map_object.get_root().html.add_child(folium.Element(MAP_STYLES))
    return map_object


def _add_hud(
    map_object: folium.Map,
    mission_status: str,
    critical_count: int,
    monitored_count: int,
    route_km: float,
    routing_source: str,
) -> None:
    engine = "Malha viária OSRM" if routing_source == "osrm" else "Trajeto estimado"
    hud_html = f"""
    <div style="
        position:fixed;top:18px;right:18px;z-index:9999;
        background:rgba(2,6,23,.9);color:#f8fafc;
        padding:14px 16px;border-radius:14px;
        border:1px solid rgba(52,211,153,.2);
        font-family:Inter,sans-serif;min-width:220px;
        box-shadow:0 16px 40px rgba(0,0,0,.45);
        backdrop-filter:blur(14px);
    ">
        <div style="font-size:10px;letter-spacing:1.2px;color:#94a3b8;font-weight:700;">STATUS OPERACIONAL</div>
        <div style="font-size:16px;font-weight:800;margin:6px 0;color:#34d399;">{mission_status}</div>
        <div style="font-size:11px;color:#94a3b8;line-height:1.6;">
            {engine}<br>
            Trajeto: <b style="color:#fff;">{route_km:.1f} km</b><br>
            Críticos: <b style="color:#f87171;">{critical_count}</b> ·
            Monitorados: <b style="color:#fbbf24;">{monitored_count}</b>
        </div>
    </div>
    """
    map_object.get_root().html.add_child(folium.Element(hud_html))


def _add_legend(map_object: folium.Map, routing_source: str) -> None:
    engine = "Malha viária OSRM" if routing_source == "osrm" else "Trajeto estimado"
    legend_html = f"""
    <div style="
        position:fixed;bottom:24px;left:24px;z-index:9999;
        background:rgba(2,6,23,.92);color:#f8fafc;
        padding:14px 16px;border-radius:14px;
        border:1px solid rgba(255,255,255,.1);
        font-size:12px;line-height:1.75;
        box-shadow:0 12px 32px rgba(0,0,0,.4);
        font-family:Inter,sans-serif;
    ">
        <div style="font-weight:800;font-size:13px;margin-bottom:4px;">Legenda operacional</div>
        <div style="color:#94a3b8;font-size:11px;margin-bottom:8px;">{engine}</div>
        <div><span style="color:#34d399;font-weight:700;">━━</span> Rota validada </div>
        <div><span style="color:#f87171;">╌╌</span> Trecho bloqueado</div>
        <div><span style="color:#60a5fa;">━━</span> Desvio viário</div>
        <div><span style="color:#f87171;">┄┄</span> Linha de impacto crítico</div>
        <div><span style="color:#ef4444;">●</span> Foco crítico</div>
        <div><span style="color:#f59e0b;">●</span> Foco monitorado</div>
    </div>
    """
    map_object.get_root().html.add_child(folium.Element(legend_html))


def _draw_route_glow(
    layer: folium.FeatureGroup,
    route: Route,
    color: str,
    glow_color: str,
    weight: int = 8,
    opacity: float = 1.0,
    dash_array: str | None = None,
    tooltip: str = "Rota",
    animated: bool = False,
) -> None:
    folium.PolyLine(
        route,
        color=glow_color,
        weight=weight + 6,
        opacity=0.22,
        tooltip=tooltip,
    ).add_to(layer)

    if animated:
        plugins.AntPath(
            route,
            color=color,
            pulse_color="#6ee7b7",
            weight=weight,
            opacity=opacity,
            delay=800,
            dash_array=[10, 20],
            tooltip=tooltip,
        ).add_to(layer)
    else:
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
    origin_label: str,
    destination_label: str,
) -> None:
    folium.Marker(
        route[0],
        tooltip=origin_label,
        icon=folium.DivIcon(
            html='<div class="ignis-route-marker ignis-route-marker--origin">O</div>',
            icon_size=(38, 38),
            icon_anchor=(19, 19),
        ),
    ).add_to(layer)

    folium.Marker(
        route[-1],
        tooltip=destination_label,
        icon=folium.DivIcon(
            html='<div class="ignis-route-marker ignis-route-marker--dest">D</div>',
            icon_size=(38, 38),
            icon_anchor=(19, 19),
        ),
    ).add_to(layer)


def _create_hotspot_popup(hotspot: Hotspot, is_blocking: bool) -> str:
    distance = hotspot.get("distance_km", 0)
    occurrence_status = hotspot.get("status_ocorrencia", "—")
    operational_impact = hotspot.get("impacto_operacional", "—")

    if is_blocking:
        status = "INTERFERE NA ROTA"
        color = "#ef4444"
    elif str(occurrence_status).upper() == "MONITORADO":
        status = "MONITORAMENTO — SEM INTERFERÊNCIA"
        color = "#f59e0b"
    else:
        status = "Em observação"
        color = "#f59e0b"

    return f"""
    <div style="font-family:Inter,sans-serif;min-width:200px;">
        <b>{hotspot.get('description', 'Foco')}</b><br>
        Severidade: {hotspot.get('severity', '—')}<br>
        Status: {occurrence_status}<br>
        Impacto: {operational_impact}<br>
        Sensor: {hotspot.get('sensor', '—')}<br>
        Distância à rota: {distance:.2f} km<br>
        <span style="color:{color};font-weight:700;">{status}</span>
    </div>
    """


def _add_impact_lines(
    layer: folium.FeatureGroup,
    route: Route,
    blocked_hotspots: list[Hotspot],
) -> None:
    for hotspot in blocked_hotspots:
        foco_point = (hotspot["latitude"], hotspot["longitude"])
        impact_point, _ = closest_point_on_route(route, foco_point)

        folium.PolyLine(
            [foco_point, impact_point],
            color=COLORS["impact_line"],
            weight=2,
            opacity=0.75,
            dash_array="4 8",
            tooltip="Impacto crítico na rota",
        ).add_to(layer)

        folium.Marker(
            impact_point,
            tooltip="Ponto de interferência",
            icon=folium.DivIcon(
                html='<div class="ignis-impact-point"></div>',
                icon_size=(10, 10),
                icon_anchor=(5, 5),
            ),
        ).add_to(layer)


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
                fill_opacity=0.04,
                weight=1,
                opacity=0.25,
                dash_array="4 6",
            ).add_to(zone_layer)

        folium.Marker(
            location=location,
            tooltip=hotspot.get("description", "Foco"),
            popup=folium.Popup(
                _create_hotspot_popup(hotspot, is_blocking),
                max_width=300,
            ),
            icon=folium.DivIcon(
                html=f'<div class="ignis-hotspot-marker {marker_class}"></div>',
                icon_size=(16, 16),
                icon_anchor=(8, 8),
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
    mission_status: str = "ANÁLISE",
    route_km: float = 0.0,
    detour_found: bool = False,
) -> folium.Map:
    blocked_ids = {hotspot.get("id") for hotspot in (blocked_hotspots or [])}
    display_route = validated_route or alt_route or route
    has_safe_detour = blocked and detour_found and alt_route is not None

    routes_for_bounds = [route, display_route]
    if alt_route:
        routes_for_bounds.append(alt_route)

    map_object = _create_base_map(_get_bounds(routes_for_bounds, hotspots))

    route_layer = folium.FeatureGroup(name="Trajeto operacional", show=True)
    impact_layer = folium.FeatureGroup(name="Impactos críticos", show=True)
    hotspot_layer = folium.FeatureGroup(name="Focos da view", show=True)
    zone_layer = folium.FeatureGroup(name="Zonas de exclusão", show=True)

    _add_route_markers(route_layer, display_route, origin_label, destination_label)

    if blocked:
        _draw_route_glow(
            route_layer,
            route,
            COLORS["blocked_route"],
            "#7f1d1d",
            weight=5,
            opacity=0.55 if has_safe_detour else 0.9,
            dash_array="8 12",
            tooltip="Rota original bloqueada",
        )
        _add_impact_lines(impact_layer, route, blocked_hotspots or [])

    if has_safe_detour and alt_route and alt_route != route:
        _draw_route_glow(
            route_layer,
            alt_route,
            COLORS["detour_route"],
            COLORS["detour_glow"],
            weight=6,
            opacity=0.75,
            tooltip="Desvio viário (OSRM)",
        )

    if not blocked:
        _draw_route_glow(
            route_layer,
            display_route,
            COLORS["safe_route"],
            COLORS["safe_glow"],
            weight=9,
            opacity=1.0,
            tooltip="Rota validada",
            animated=True,
        )
    elif has_safe_detour:
        _draw_route_glow(
            route_layer,
            display_route,
            COLORS["safe_route"],
            COLORS["safe_glow"],
            weight=10,
            opacity=1.0,
            tooltip="Rota validada (desvio aprovado)",
            animated=True,
        )

    _add_hotspots(hotspot_layer, zone_layer, hotspots, blocked_ids)

    route_layer.add_to(map_object)
    impact_layer.add_to(map_object)
    hotspot_layer.add_to(map_object)
    zone_layer.add_to(map_object)

    folium.LayerControl(collapsed=True).add_to(map_object)
    plugins.Fullscreen(position="topright").add_to(map_object)

    monitored_count = sum(
        1 for hotspot in hotspots if str(hotspot.get("status_ocorrencia", "")).upper() == "MONITORADO"
    )
    _add_hud(
        map_object,
        mission_status,
        len(blocked_hotspots or []),
        monitored_count,
        route_km,
        routing_source,
    )
    _add_legend(map_object, routing_source)

    return map_object


def export_map_html(map_object: folium.Map, path: str) -> str:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    map_object.save(str(output))
    return str(output)
