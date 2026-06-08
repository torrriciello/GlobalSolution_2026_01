"""Focos de calor padrão — Região Metropolitana de São Paulo (modo demonstração)."""

from typing import Dict, List

Hotspot = Dict[str, object]

DEFAULT_HOTSPOTS: List[Hotspot] = [
    {
        "id": 1,
        "latitude": -23.5780,
        "longitude": -46.6410,
        "severity": "Alto",
        "description": "Foco em Vila Mariana (leste)",
        "sensor": "MODIS-DEMO",
        "distance_km": 0.0,
        "affected_radius_m": 5000.0,
        "date": "2026-06-06",
    },
    {
        "id": 2,
        "latitude": -23.5473,
        "longitude": -46.5498,
        "severity": "Médio",
        "description": "Fumaça em Tatuapé",
        "sensor": "VIIRS-DEMO",
        "distance_km": 0.0,
        "affected_radius_m": 3000.0,
        "date": "2026-06-06",
    },
    {
        "id": 3,
        "latitude": -23.5615,
        "longitude": -46.7058,
        "severity": "Baixo",
        "description": "Fogo em Pinheiros",
        "sensor": "MODIS-DEMO",
        "distance_km": 0.0,
        "affected_radius_m": 2000.0,
        "date": "2026-06-06",
    },
]
