"""Agregações analíticas a partir dos registros da view de focos."""

from dataclasses import dataclass
from typing import Any

import pandas as pd

SEVERITY_WEIGHTS = {
    "crítico": 4,
    "critico": 4,
    "alto": 3,
    "médio": 2,
    "medio": 2,
    "baixo": 1,
}

SEVERITY_ORDER = ["Crítico", "Alto", "Médio", "Baixo"]


def severity_to_risk_level(severity: str) -> str:
    mapping = {
        "Crítico": "CRÍTICO",
        "Alto": "ALTO",
        "Médio": "MODERADO",
        "Baixo": "BAIXO",
        "—": "BAIXO",
    }
    return mapping.get(_normalize_severity(severity), "MODERADO")


@dataclass
class OperationalMetrics:
    total_foci: int
    active_foci: int
    monitored_foci: int
    active_sensors: int
    max_severity: str
    avg_distance_km: float
    risk_index: float
    avg_interdiction_min: float
    interfering_count: int


def _normalize_severity(value: str) -> str:
    key = str(value).strip().lower()
    mapping = {
        "critico": "Crítico",
        "crítico": "Crítico",
        "alto": "Alto",
        "medio": "Médio",
        "médio": "Médio",
        "baixo": "Baixo",
    }
    return mapping.get(key, str(value).strip() or "Médio")


def compute_operational_metrics(
    foci: list[dict[str, Any]],
    interfering_count: int = 0,
) -> OperationalMetrics:
    if not foci:
        return OperationalMetrics(
            total_foci=0,
            active_foci=0,
            monitored_foci=0,
            active_sensors=0,
            max_severity="—",
            avg_distance_km=0.0,
            risk_index=0.0,
            avg_interdiction_min=0.0,
            interfering_count=interfering_count,
        )

    severities = [_normalize_severity(f.get("severity", "Médio")) for f in foci]
    sensors = {str(f.get("sensor", "")).strip() for f in foci if f.get("sensor")}
    distances = [float(f.get("distance_km", 0)) for f in foci]
    interdictions = [float(f.get("interdiction_min", 0)) for f in foci if f.get("interdiction_min")]

    max_severity = "Baixo"
    max_weight = 0
    for severity in severities:
        weight = SEVERITY_WEIGHTS.get(severity.lower(), 1)
        if weight > max_weight:
            max_weight = weight
            max_severity = severity

    total_weight = sum(SEVERITY_WEIGHTS.get(s.lower(), 1) for s in severities)
    max_possible = len(foci) * max(SEVERITY_WEIGHTS.values())
    risk_index = round((total_weight / max_possible) * 100, 1) if max_possible else 0.0

    active_foci = sum(
        1 for foco in foci if str(foco.get("status_ocorrencia", "")).upper() == "ATIVO"
    )
    monitored_foci = sum(
        1 for foco in foci if str(foco.get("status_ocorrencia", "")).upper() == "MONITORADO"
    )

    return OperationalMetrics(
        total_foci=len(foci),
        active_foci=active_foci,
        monitored_foci=monitored_foci,
        active_sensors=len(sensors),
        max_severity=max_severity,
        avg_distance_km=round(sum(distances) / len(distances), 2) if distances else 0.0,
        risk_index=risk_index,
        avg_interdiction_min=round(sum(interdictions) / len(interdictions), 1) if interdictions else 0.0,
        interfering_count=interfering_count,
    )


def severity_distribution(foci: list[dict[str, Any]]) -> pd.DataFrame:
    if not foci:
        return pd.DataFrame({"Severidade": SEVERITY_ORDER, "Focos": [0] * len(SEVERITY_ORDER)})

    counts: dict[str, int] = {level: 0 for level in SEVERITY_ORDER}
    for foco in foci:
        label = _normalize_severity(foco.get("severity", "Médio"))
        if label not in counts:
            counts[label] = 0
        counts[label] += 1

    rows = [(level, counts.get(level, 0)) for level in SEVERITY_ORDER if counts.get(level, 0)]
    extras = [(level, count) for level, count in counts.items() if level not in SEVERITY_ORDER and count]
    rows.extend(extras)

    return pd.DataFrame(rows, columns=["Severidade", "Focos"]).set_index("Severidade")


def sensor_distribution(foci: list[dict[str, Any]]) -> pd.DataFrame:
    if not foci:
        return pd.DataFrame(columns=["Sensor", "Detecções"])

    counts: dict[str, int] = {}
    for foco in foci:
        sensor = str(foco.get("sensor", "Desconhecido")).strip() or "Desconhecido"
        counts[sensor] = counts.get(sensor, 0) + 1

    rows = sorted(counts.items(), key=lambda item: item[1], reverse=True)
    return pd.DataFrame(rows, columns=["Sensor", "Detecções"]).set_index("Sensor")


def focos_dataframe(foci: list[dict[str, Any]]) -> pd.DataFrame:
    if not foci:
        return pd.DataFrame(
            columns=[
                "ID",
                "Local",
                "Severidade",
                "Status",
                "Impacto",
                "Sensor",
                "Distância à rota (km)",
                "Raio afetado (m)",
                "Interdição est. (min)",
                "Data",
            ]
        )

    rows = []
    for foco in foci:
        rows.append(
            {
                "ID": foco.get("id"),
                "Local": foco.get("description", "—"),
                "Severidade": _normalize_severity(foco.get("severity", "—")),
                "Sensor": foco.get("sensor", "—"),
                "Distância à rota (km)": foco.get("distance_km", 0),
                "Raio afetado (m)": foco.get("affected_radius_m", 0),
                "Interdição est. (min)": foco.get("interdiction_min") or "—",
                "Status": foco.get("status_ocorrencia", "—"),
                "Impacto": foco.get("impacto_operacional", "—"),
                "Data": foco.get("date", "—"),
            }
        )

    return pd.DataFrame(rows)
