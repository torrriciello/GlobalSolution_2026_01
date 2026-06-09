from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from models.route_result import RouteAnalysisResult
from services.analytics_service import OperationalMetrics, severity_to_risk_level

RiskLevel = Literal["BAIXO", "MODERADO", "ALTO", "CRÍTICO"]
DecisionAction = Literal["PROSSEGUIR", "DESVIAR", "REAVALIAR", "AGUARDAR"]


@dataclass(frozen=True)
class ImpactReason:
    title: str
    detail: str
    severity: str
    sensor: str
    distance_km: float


@dataclass(frozen=True)
class MissionContext:
    risk_level: RiskLevel
    decision: DecisionAction
    decision_title: str
    decision_detail: str
    mission_status: str
    alert_type: str
    alert_message: str
    narrative_summary: str
    impact_reasons: tuple[ImpactReason, ...] = field(default_factory=tuple)


def _build_impact_reasons(result: RouteAnalysisResult) -> tuple[ImpactReason, ...]:
    reasons = []
    for foco in result.interfering_foci:
        reasons.append(
            ImpactReason(
                title=str(foco.get("description", "Foco ativo")),
                detail=(
                    f"Status {foco.get('status_ocorrencia', 'ATIVO')} · "
                    f"impacto {foco.get('impacto_operacional', '—')} · "
                    f"distância {foco.get('distance_km', 0):.2f} km à rota · "
                    f"raio efetivo {foco.get('effective_radius_km', 0):.2f} km"
                ),
                severity=str(foco.get("severity", "—")),
                sensor=str(foco.get("sensor", "—")),
                distance_km=float(foco.get("distance_km", 0)),
            )
        )
    return tuple(reasons)


def build_mission_context(
    result: RouteAnalysisResult,
    metrics: OperationalMetrics,
    radius_km: float,
) -> MissionContext:
    impact_reasons = _build_impact_reasons(result)

    if result.scenario.strip().lower() in {"via livre", "livre"}:
        return MissionContext(
            risk_level="BAIXO",
            decision="PROSSEGUIR",
            decision_title="Trajeto liberado",
            decision_detail="Análise executada sem carregar focos da view analítica.",
            mission_status="OPERACIONAL",
            alert_type="success",
            alert_message=f"Margem de segurança de {radius_km} km aplicada sobre a malha viária.",
            narrative_summary=(
                "Nenhum foco da base foi considerado nesta execução. "
                "A rota viária foi validada apenas contra parâmetros operacionais."
            ),
        )

    if result.is_free:
        risk_level = severity_to_risk_level(metrics.max_severity)
        return MissionContext(
            risk_level=risk_level,
            decision="PROSSEGUIR",
            decision_title="Rota viária validada",
            decision_detail=(
                f"{metrics.total_foci} foco(s) operacionais em vw_focos_ativos, nenhum ATIVO na margem de {radius_km} km. "
                f"Severidade máxima registrada: {metrics.max_severity}."
            ),
            mission_status="MONITORAMENTO ATIVO",
            alert_type="success",
            alert_message=(
                f"Trajeto liberado — {metrics.total_foci} foco(s) monitorados "
                f"a distância média de {metrics.avg_distance_km:.1f} km."
            ),
            narrative_summary=(
                f"A malha viária não intercepta zonas críticas. "
                f"{metrics.active_sensors} sensor(es) reportando atividade no cenário."
            ),
        )

    if result.detour_found:
        extra_km = (result.detour_distance_km or 0) - result.route_distance_km
        critical_names = ", ".join(reason.title for reason in impact_reasons[:3])
        return MissionContext(
            risk_level="ALTO",
            decision="DESVIAR",
            decision_title="Desvio tático necessário",
            decision_detail=(
                f"{metrics.interfering_count} foco(s) críticos bloqueiam a rota original "
                f"(ex.: {critical_names}). Desvio validado com +{max(extra_km, 0):.1f} km."
            ),
            mission_status="DESVIO ATIVO",
            alert_type="warning",
            alert_message=(
                f"Interdição térmica detectada — {metrics.interfering_count} foco(s) "
                f"dentro da margem de {radius_km} km."
            ),
            narrative_summary=(
                "A rota original cruza zonas de exclusão derivadas dos focos ativos. "
                "O desvio viário alternativo foi calculado para preservar a segurança operacional."
            ),
            impact_reasons=impact_reasons,
        )

    critical_names = ", ".join(reason.title for reason in impact_reasons[:3]) or "focos críticos"
    return MissionContext(
        risk_level="CRÍTICO",
        decision="REAVALIAR",
        decision_title="Bloqueio operacional",
        decision_detail=(
            f"{metrics.interfering_count} foco(s) críticos ({critical_names}) impedem a rota "
            "e nenhum desvio viário seguro foi encontrado."
        ),
        mission_status="MISSÃO INTERROMPIDA",
        alert_type="danger",
        alert_message="Missão interrompida — nenhum desvio viário seguro encontrado via OSRM.",
        narrative_summary=(
            "Todos os trajetos viários avaliados permanecem dentro de zonas de risco "
            "calculadas a partir dos registros da view analítica."
        ),
        impact_reasons=impact_reasons,
    )


def current_timestamp() -> str:
    return datetime.now().strftime("%d/%m/%Y  %H:%M")
