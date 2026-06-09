from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple

Coordinate = Tuple[float, float]
Route = List[Coordinate]

RoadStatus = Literal["LIVRE", "INTERDITADA"]


@dataclass(slots=True)
class RouteAnalysisResult:
    """
    Resultado consolidado da análise tática da rota.
    """

    road_status: RoadStatus

    interfering_foci_count: int
    monitored_foci_count: int

    validated_route: Route
    original_route: Route
    detour_route: Optional[Route]

    interfering_foci: List[Dict[str, Any]] = field(default_factory=list)
    monitored_foci: List[Dict[str, Any]] = field(default_factory=list)

    scenario: str = ""
    safety_radius_km: float = 0.0

    route_distance_km: float = 0.0
    detour_distance_km: Optional[float] = None

    database_connected: bool = False
    data_source: str = "fallback"
    connection_error: Optional[str] = None

    map_html_path: Optional[str] = None
    detour_found: bool = True

    routing_source: str = "osrm"
    route_duration_min: float = 0.0
    detour_duration_min: Optional[float] = None

    # =====================================================
    # Computed Properties
    # =====================================================

    @property
    def is_blocked(self) -> bool:
        return self.road_status == "INTERDITADA"

    @property
    def is_free(self) -> bool:
        return self.road_status == "LIVRE"

    @property
    def has_detour(self) -> bool:
        return self.detour_found and self.detour_route is not None

    @property
    def effective_route(self) -> Route:
        """
        Retorna a rota efetivamente utilizada.
        """

        return self.validated_route

    @property
    def display_distance(self) -> float:
        """
        Distância exibida na UI.
        """

        return (
            self.detour_distance_km
            if self.detour_distance_km is not None
            else self.route_distance_km
        )

    @property
    def status_label(self) -> str:
        return "Livre" if self.is_free else "Interditada"

    @property
    def status_css(self) -> str:
        return (
            "status-livre"
            if self.is_free
            else "status-interditada"
        )

    # =====================================================
    # Helpers
    # =====================================================

    def coordinate_matrix(self) -> List[List[float]]:
        """
        Converte rota para formato serializável.
        """

        return [
            [lat, lon]
            for lat, lon in self.validated_route
        ]

    def summary(self) -> Dict[str, Any]:
        """
        Resumo simplificado para dashboards.
        """

        return {
            "status": self.road_status,
            "focos_interferindo": self.interfering_foci_count,
            "focos_monitorados": self.monitored_foci_count,
            "distancia_km": self.display_distance,
            "desvio_encontrado": self.detour_found,
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)