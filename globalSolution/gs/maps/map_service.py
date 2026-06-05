import folium


def build_route_map(route, hotspots, radius_km, alt_route=None, blocked=False):
    center_lat = sum(point[0] for point in route) / len(route)
    center_lon = sum(point[1] for point in route) / len(route)

    map_object = folium.Map(location=(center_lat, center_lon), zoom_start=11, control_scale=True)

    folium.Marker(route[0], tooltip="Origem", icon=folium.Icon(color="green", icon="play")).add_to(map_object)
    folium.Marker(route[-1], tooltip="Destino", icon=folium.Icon(color="red", icon="flag")).add_to(map_object)

    route_color = "green" if not blocked else "red"
    folium.PolyLine(route, color=route_color, weight=6, opacity=0.8, tooltip="Rota principal").add_to(map_object)

    if alt_route:
        folium.PolyLine(alt_route, color="blue", weight=4, opacity=0.9, dash_array="8", tooltip="Rota alternativa").add_to(map_object)

    for hotspot in hotspots:
        location = (hotspot["latitude"], hotspot["longitude"])
        folium.Circle(
            location=location,
            radius=radius_km * 1000,
            color="orange",
            fill=True,
            fill_opacity=0.2,
            tooltip=f"{hotspot.get('description', 'Foco de incêndio')} ({hotspot.get('severity', 'Desconhecida')})",
        ).add_to(map_object)
        folium.Marker(
            location=location,
            tooltip=f"Hotspot: {hotspot.get('description', 'Foco de incêndio')}",
            icon=folium.Icon(color="darkred", icon="fire" if not blocked else "exclamation-triangle", prefix="fa"),
        ).add_to(map_object)

    return map_object
