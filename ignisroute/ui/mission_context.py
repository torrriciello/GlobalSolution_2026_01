from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from models.route_result import RouteAnalysisResult

RiskLevel = Literal["BAIXO", "MODERADO", "ALTO", "CRÍTICO"]
DecisionAction = Literal["PROSSEGUIR", "DESVIAR", "REAVALIAR", "AGUARDAR"]


@dataclass(frozen=True)
class MissionContext:
    risk_level: RiskLevel
    decision: DecisionAction
    decision_title: str
    decision_detail: str
    mission_status: str
    estimated_response_min: float
    containment_index: float
    diversion_rate: float
    alert_type: str
    alert_message: str


def _estimate_response_minutes(distance_km: float) -> float:
    avg_speed_kmh = 55.0
    return round((distance_km / avg_speed_kmh) * 60, 1)


def build_mission_context(result: RouteAnalysisResult, radius_km: float) -> MissionContext:
    distance = result.display_distance
    response_min = _estimate_response_minutes(distance)

    if result.scenario.strip().lower() in {"via livre", "livre"}:
        return MissionContext(
            risk_level="BAIXO",
            decision="PROSSEGUIR",
            decision_title="Rota principal autorizada",
            decision_detail=(
                "Cenário sem ameaças térmicas ativas. A viatura pode seguir o trajeto "
                "planejado com monitoramento padrão."
            ),
            mission_status="OPERACIONAL",
            estimated_response_min=response_min,
            containment_index=100.0,
            diversion_rate=0.0,
            alert_type="success",
            alert_message=(
                f"Trajeto validado — nenhum foco interfere no raio de {radius_km} km."
            ),
        )

    if result.is_free:
        return MissionContext(
            risk_level="MODERADO",
            decision="PROSSEGUIR",
            decision_title="Rota validada com monitoramento",
            decision_detail=(
                f"{result.monitored_foci_count} foco(s) monitorado(s), "
                "porém fora da zona de exclusão. Manter vigilância contínua."
            ),
            mission_status="MONITORAMENTO ATIVO",
            estimated_response_min=response_min,
            containment_index=100.0,
            diversion_rate=0.0,
            alert_type="success",
            alert_message=(
                f"Rota liberada — {result.monitored_foci_count} foco(s) sob observação."
            ),
        )

    if result.detour_found:
        extra_km = (result.detour_distance_km or 0) - result.route_distance_km
        return MissionContext(
            risk_level="ALTO",
            decision="DESVIAR",
            decision_title="Desvio tático autorizado",
            decision_detail=(
                f"{result.interfering_foci_count} foco(s) cruzam a rota original. "
                f"Trajeto alternativo validado (+{max(extra_km, 0):.1f} km)."
            ),
            mission_status="DESVIO ATIVO",
            estimated_response_min=response_min,
            containment_index=100.0,
            diversion_rate=round(
                (extra_km / result.route_distance_km * 100) if result.route_distance_km else 0,
                1,
            ),
            alert_type="warning",
            alert_message=(
                f"Rota principal interditada — {result.interfering_foci_count} foco(s) "
                f"dentro do raio de {radius_km} km. Desvio seguro calculado."
            ),
        )

    return MissionContext(
        risk_level="CRÍTICO",
        decision="REAVALIAR",
        decision_title="Interdição sem desvio viável",
        decision_detail=(
            "Nenhum trajeto alternativo seguro foi encontrado. "
            "Recomenda-se aguardar contenção ou ampliar parâmetros operacionais."
        ),
        mission_status="BLOQUEIO TOTAL",
        estimated_response_min=0.0,
        containment_index=0.0,
        diversion_rate=100.0,
        alert_type="danger",
        alert_message=(
            "Rota bloqueada e desvio indisponível. Missão requer reavaliação imediata."
        ),
    )


def current_timestamp() -> str:
    return datetime.now().strftime("%d/%m/%Y  %H:%M")
