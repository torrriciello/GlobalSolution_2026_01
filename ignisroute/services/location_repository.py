"""Carregamento de localidades operacionais a partir das dimensões geográficas."""

import logging
import os
from dataclasses import dataclass

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from supabase import create_client

from data.hotspots import DEFAULT_HOTSPOTS
from services.db_connection import (
    build_supabase_rest_url,
    connection_kwargs,
    extract_supabase_project_ref,
    friendly_connection_error,
)
from services.hotspot_repository import VIEW_NAME

load_dotenv()

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DB_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

LOCATIONS_QUERY = """
    SELECT
        m.id_municipio,
        m.nome_municipio,
        e.uf,
        e.nome_estado,
        AVG(rg.latitude)::float8 AS latitude,
        AVG(rg.longitude)::float8 AS longitude
    FROM dim_municipio m
    INNER JOIN dim_estado e ON e.id_estado = m.id_estado
    INNER JOIN dim_regiao_geografica rg ON rg.id_municipio = m.id_municipio
    GROUP BY m.id_municipio, m.nome_municipio, e.uf, e.nome_estado
    ORDER BY m.nome_municipio
"""

REGION_QUERY = """
    SELECT string_agg(DISTINCT e.nome_estado || ' (' || e.uf || ')', ', ' ORDER BY e.nome_estado || ' (' || e.uf || ')') AS region
    FROM dim_municipio m
    INNER JOIN dim_estado e ON e.id_estado = m.id_estado
    INNER JOIN dim_regiao_geografica rg ON rg.id_municipio = m.id_municipio
"""


@dataclass
class OperationalLocation:
    id: int
    name: str
    municipality: str
    uf: str
    state: str
    lat: float
    lon: float


@dataclass
class LocationLoadResult:
    locations: list[OperationalLocation]
    connected: bool
    source: str
    region_label: str
    error: str | None = None


def _build_location(record: dict) -> OperationalLocation:
    municipality = str(record["nome_municipio"]).strip()
    uf = str(record["uf"]).strip()
    return OperationalLocation(
        id=int(record["id_municipio"]),
        name=f"{municipality} — {uf}",
        municipality=municipality,
        uf=uf,
        state=str(record.get("nome_estado", "")).strip(),
        lat=float(record["latitude"]),
        lon=float(record["longitude"]),
    )


def _region_from_locations(locations: list[OperationalLocation]) -> str:
    states = sorted({f"{loc.state} ({loc.uf})" for loc in locations if loc.state and loc.uf})
    return ", ".join(states) if states else "Área não definida"


def _fallback_from_hotspots() -> list[OperationalLocation]:
    seen: set[str] = set()
    locations: list[OperationalLocation] = []

    for index, hotspot in enumerate(DEFAULT_HOTSPOTS, start=1):
        description = str(hotspot.get("description", f"Local {index}")).strip()
        if description in seen:
            continue
        seen.add(description)

        parts = description.split(" - ")
        municipality = parts[0].strip()
        uf = parts[-1].strip() if len(parts) > 1 else "—"

        locations.append(
            OperationalLocation(
                id=index,
                name=description.replace(" - ", " — ") if " - " in description else description,
                municipality=municipality,
                uf=uf,
                state=uf,
                lat=float(hotspot["latitude"]),
                lon=float(hotspot["longitude"]),
            )
        )

    return locations


def _resolve_supabase_rest_url() -> str:
    if SUPABASE_URL and SUPABASE_URL.startswith("https://"):
        return SUPABASE_URL.rstrip("/").replace("/rest/v1", "")

    if DATABASE_URL:
        try:
            params = connection_kwargs(DATABASE_URL)
            project_ref = extract_supabase_project_ref(params["host"], params.get("user"))
            if project_ref:
                return build_supabase_rest_url(project_ref)
        except ValueError:
            pass

    return ""


def _fetch_from_postgresql(database_url: str) -> tuple[list[OperationalLocation], str]:
    kwargs = connection_kwargs(database_url)
    kwargs["cursor_factory"] = RealDictCursor

    with psycopg2.connect(**kwargs) as connection:
        with connection.cursor() as cursor:
            cursor.execute(LOCATIONS_QUERY)
            rows = cursor.fetchall()
            locations = [_build_location(row) for row in rows]

            region_label = _region_from_locations(locations)
            try:
                cursor.execute(REGION_QUERY)
                region_row = cursor.fetchone()
                if region_row and region_row.get("region"):
                    region_label = str(region_row["region"])
            except Exception:
                pass

    logger.info("PostgreSQL carregou %s localidades", len(locations))
    return locations, region_label


def _fetch_from_supabase(rest_url: str) -> tuple[list[OperationalLocation], str]:
    client = create_client(rest_url, SUPABASE_KEY)
    response = client.table(VIEW_NAME).select("description,latitude,longitude").execute()
    records = getattr(response, "data", [])

    seen: set[str] = set()
    locations: list[OperationalLocation] = []

    for index, record in enumerate(records, start=1):
        description = str(record.get("description", "")).strip()
        if not description or description in seen:
            continue
        seen.add(description)

        parts = description.split(" - ")
        municipality = parts[0].strip()
        uf = parts[-1].strip() if len(parts) > 1 else "—"

        locations.append(
            OperationalLocation(
                id=index,
                name=f"{municipality} — {uf}",
                municipality=municipality,
                uf=uf,
                state=uf,
                lat=float(record["latitude"]),
                lon=float(record["longitude"]),
            )
        )

    locations.sort(key=lambda item: item.name)
    region_label = _region_from_locations(locations)
    logger.info("Supabase REST carregou %s localidades", len(locations))
    return locations, region_label


def load_locations() -> LocationLoadResult:
    """
    Estratégia de obtenção:
    1. PostgreSQL — dim_municipio + dim_regiao_geografica + dim_estado
    2. Supabase REST — localidades distintas da view de focos
    3. Dataset local derivado dos focos de demonstração
    """
    last_error: str | None = None
    rest_url = _resolve_supabase_rest_url()

    if DATABASE_URL:
        try:
            locations, region_label = _fetch_from_postgresql(DATABASE_URL)
            if locations:
                return LocationLoadResult(locations, True, "postgresql", region_label)
            last_error = "Nenhuma localidade encontrada nas dimensões geográficas."
            logger.warning(last_error)
        except Exception as error:
            host = None
            try:
                host = connection_kwargs(DATABASE_URL).get("host")
            except ValueError:
                pass
            last_error = friendly_connection_error(error, host)
            logger.warning("PostgreSQL indisponível para localidades: %s", last_error)

    if rest_url and SUPABASE_KEY:
        try:
            locations, region_label = _fetch_from_supabase(rest_url)
            if locations:
                return LocationLoadResult(locations, True, "supabase", region_label, last_error)
            last_error = "Supabase REST: nenhuma localidade retornada."
            logger.warning(last_error)
        except Exception as error:
            last_error = f"Supabase REST: {error}"
            logger.warning(last_error)

    fallback = _fallback_from_hotspots()
    return LocationLoadResult(
        locations=fallback,
        connected=False,
        source="fallback",
        region_label=_region_from_locations(fallback),
        error=last_error,
    )


def find_location(locations: list[OperationalLocation], label: str) -> OperationalLocation | None:
    for location in locations:
        if location.name == label:
            return location
    return None
