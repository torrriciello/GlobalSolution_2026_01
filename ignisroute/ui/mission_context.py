from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from models.route_result import RouteAnalysisResult
from services.analytics_service import OperationalMetrics, severity_to_risk_level

RiskLevel = Literal["BAIXO", "MODERADO", "ALTO", "CRÍTICO"]
DecisionAction = Literal["PROSSEGUIR", "DESVIAR", "REAVALIAR", "AGUARDAR"]


@dataclass(frozen=True)
class MissionContext:
    risk_level: RiskLevel
    decision: DecisionAction
    decision_title: str
    decision_detail: str
    mission_status: str
    alert_type: str
    alert_message: str


def build_mission_context(
    result: RouteAnalysisResult,
    metrics: OperationalMetrics,
    radius_km: float,
) -> MissionContext:
    if result.scenario.strip().lower() in {"via livre", "livre"}:
        return MissionContext(
            risk_level="BAIXO",
            decision="PROSSEGUIR",
            decision_title="Rota principal autorizada",
            decision_detail=(
                "Cenário sem focos ativos na base analítica. "
                "Trajeto validado com monitoramento padrão."
            ),
            mission_status="OPERACIONAL",
            alert_type="success",
            alert_message=f"Trajeto liberado — margem de segurança de {radius_km} km aplicada.",
        )

    if result.is_free:
        risk_level = severity_to_risk_level(metrics.max_severity)
        return MissionContext(
            risk_level=risk_level,
            decision="PROSSEGUIR",
            decision_title="Rota validada com monitoramento",
            decision_detail=(
                f"{metrics.total_foci} foco(s) ativos na view, "
                f"{metrics.interfering_count} interferindo na rota. "
                f"Severidade máxima: {metrics.max_severity}."
            ),
            mission_status="MONITORAMENTO ATIVO",
            alert_type="success",
            alert_message=(
                f"Rota liberada — {metrics.total_foci} foco(s) monitorados, "
                f"distância média {metrics.avg_distance_km:.1f} km."
            ),
        )

    if result.detour_found:
        extra_km = (result.detour_distance_km or 0) - result.route_distance_km
        return MissionContext(
            risk_level="ALTO",
            decision="DESVIAR",
            decision_title="Desvio tático autorizado",
            decision_detail=(
                f"{metrics.interfering_count} foco(s) críticos na rota original. "
                f"Desvio validado com {result.display_distance:.1f} km "
                f"(+{max(extra_km, 0):.1f} km)."
            ),
            mission_status="DESVIO ATIVO",
            alert_type="warning",
            alert_message=(
                f"Rota interditada — {metrics.interfering_count} foco(s) dentro da margem "
                f"de {radius_km} km. Trajeto alternativo calculado."
            ),
        )

    return MissionContext(
        risk_level="CRÍTICO",
        decision="REAVALIAR",
        decision_title="Interdição sem desvio viável",
        decision_detail=(
            f"{metrics.interfering_count} foco(s) críticos bloqueiam a rota e nenhum "
            "trajeto alternativo seguro foi encontrado na análise."
        ),
        mission_status="BLOQUEIO TOTAL",
        alert_type="danger",
        alert_message=(
            "Rota bloqueada e desvio indisponível. Reavaliar missão com base nos focos ativos."
        ),
    )


def current_timestamp() -> str:
    return datetime.now().strftime("%d/%m/%Y  %H:%M")
