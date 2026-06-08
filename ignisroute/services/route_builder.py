"""Construção de rotas operacionais sobre a malha viária."""

from services.routing_service import Coordinate, RoutedPath, fetch_road_route


def build_mission_route(origin: Coordinate, destination: Coordinate) -> RoutedPath:
    """Calcula a rota viária entre origem e destino."""
    return fetch_road_route([origin, destination])
