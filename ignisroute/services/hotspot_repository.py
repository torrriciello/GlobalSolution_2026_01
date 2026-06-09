import logging
import os
from dataclasses import dataclass
from typing import Final

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from supabase import Client, create_client

from data.hotspots import Hotspot
from services.db_connection import (
    build_supabase_rest_url,
    connection_kwargs,
    extract_supabase_project_ref,
    friendly_connection_error,
)

load_dotenv()

logger = logging.getLogger(__name__)

VIEW_NAME: Final[str] = "vw_focos_ativos"

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("DB_URL")


@dataclass
class HotspotLoadResult:
    hotspots: list[Hotspot]
    connected: bool
    source: str
    error: str | None = None


def _resolve_supabase_rest_url() -> str:

    if DATABASE_URL:
        try:
            params = connection_kwargs(DATABASE_URL)
            project_ref = extract_supabase_project_ref(
                params["host"],
                params.get("user"),
            )
            if project_ref:
                return build_supabase_rest_url(project_ref)
        except ValueError:
            pass

    return ""


def _build_description(record: dict) -> str:
    municipality = str(record.get("nome_municipio", "")).strip()
    uf = str(record.get("uf", "")).strip()
    if municipality and uf:
        return f"{municipality} - {uf}"
    return str(record.get("description", "Foco operacional")).strip() or "Foco operacional"


def _build_hotspot(record: dict) -> Hotspot:
    return {
        "id": record["id_fato"],
        "latitude": float(record["latitude"]),
        "longitude": float(record["longitude"]),
        "severity": record["severity"],
        "description": _build_description(record),
        "sensor": record["nome_sensor"],
        "status_ocorrencia": str(record.get("status_ocorrencia", "ATIVO")).strip().upper(),
        "impacto_operacional": str(record.get("impacto_operacional", "MONITORAMENTO")).strip().upper(),
        "distance_km": float(record.get("distancia_risco_km") or 0),
        "affected_radius_m": float(record.get("raio_afetado_metros") or 0),
        "interdiction_min": float(record.get("tempo_interdicao_minutos") or 0) or None,
        "date": str(record["data_completa"]),
    }


def _fetch_from_postgresql(database_url: str) -> list[Hotspot]:
    query = f"""
        SELECT
            id_fato,
            latitude,
            longitude,
            severity,
            nome_municipio,
            uf,
            nome_sensor,
            status_ocorrencia,
            impacto_operacional,
            distancia_risco_km,
            raio_afetado_metros,
            tempo_interdicao_minutos,
            data_completa
        FROM {VIEW_NAME}
    """

    kwargs = connection_kwargs(database_url)
    kwargs["cursor_factory"] = RealDictCursor

    with psycopg2.connect(**kwargs) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            hotspots = [_build_hotspot(row) for row in cursor.fetchall()]

    logger.info("PostgreSQL carregou %s hotspots", len(hotspots))
    return hotspots


def _create_supabase_client(rest_url: str) -> Client:
    return create_client(rest_url, SUPABASE_KEY)


def _fetch_from_supabase(rest_url: str) -> list[Hotspot]:
    client = _create_supabase_client(rest_url)
    response = client.table(VIEW_NAME).select("*").execute()
    records = getattr(response, "data", [])
    hotspots = [_build_hotspot(record) for record in records]
    logger.info("Supabase REST carregou %s hotspots", len(hotspots))
    return hotspots


def get_hotspots() -> tuple[list[Hotspot], bool, str]:
    """Compatível com código legado — retorna (hotspots, connected, source)."""
    result = load_hotspots()
    return result.hotspots, result.connected, result.source


def load_hotspots() -> HotspotLoadResult:
    """
    Estratégia de obtenção:
    1. PostgreSQL direto
    2. Supabase REST (HTTPS — funciona sem IPv6)
    3. Dataset local de demonstração
    """
    last_error: str | None = None
    rest_url = _resolve_supabase_rest_url()

    if DATABASE_URL:
        try:
            hotspots = _fetch_from_postgresql(DATABASE_URL)
            if hotspots:
                return HotspotLoadResult(hotspots, True, "postgresql")
            last_error = f"A view {VIEW_NAME} não retornou registros."
            logger.warning(last_error)
        except Exception as error:
            host = None
            try:
                host = connection_kwargs(DATABASE_URL).get("host")
            except ValueError:
                pass
            last_error = friendly_connection_error(error, host)
            logger.warning("PostgreSQL indisponível: %s", last_error)

    if rest_url and SUPABASE_KEY:
        try:
            hotspots = _fetch_from_supabase(rest_url)
            if hotspots:
                return HotspotLoadResult(hotspots, True, "supabase", last_error)
            last_error = f"Supabase REST: {VIEW_NAME} retornou vazio."
            logger.warning(last_error)
        except Exception as error:
            last_error = f"Supabase REST: {error}"
            logger.warning(last_error)
    elif rest_url and not SUPABASE_KEY:
        hint = (
            "SUPABASE_KEY não configurada. Adicione a chave anon/service do painel Supabase "
            "para fallback via API REST quando PostgreSQL direto falhar."
        )
        last_error = last_error or hint
        logger.warning(hint)

    logger.warning("Base indisponível — nenhum foco carregado.")
    return HotspotLoadResult(
        hotspots=[],
        connected=False,
        source="unavailable",
        error=last_error or "Conexão com PostgreSQL necessária para carregar vw_focos_ativos.",
    )
