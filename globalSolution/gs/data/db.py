import os
from typing import Dict, List, Tuple

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()

Hotspot = Dict[str, object]
Route = List[Tuple[float, float]]

DEFAULT_HOTSPOTS: List[Hotspot] = [
    {
        "id": 1,
        "latitude": -23.5934,
        "longitude": -46.6305,
        "description": "Foco em Vila Mariana",
        "severity": "Alto",
    },
    {
        "id": 2,
        "latitude": -23.5473,
        "longitude": -46.5498,
        "description": "Fumaça em Tatuapé",
        "severity": "Médio",
    },
    {
        "id": 3,
        "latitude": -23.5615,
        "longitude": -46.7058,
        "description": "Queimada em Pinheiros",
        "severity": "Alto",
    },
]


def _get_database_url() -> str | None:
    return os.getenv("DB_URL") or os.getenv("DATABASE_URL")


def _fetch_hotspots_from_db(database_url: str) -> List[Hotspot]:
    connect_kwargs = {
        "dsn": database_url,
        "cursor_factory": RealDictCursor,
    }

    if "supabase.com" in database_url:
        connect_kwargs["sslmode"] = "require"

    with psycopg2.connect(**connect_kwargs) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT id, latitude, longitude, description, severity FROM hotspots "
                "WHERE latitude IS NOT NULL AND longitude IS NOT NULL"
            )
            return [dict(row) for row in cursor.fetchall()]


def get_hotspots() -> tuple[List[Hotspot], bool]:
    database_url = _get_database_url()
    if not database_url:
        return DEFAULT_HOTSPOTS, False

    try:
        hotspots = _fetch_hotspots_from_db(database_url)
        return (hotspots or DEFAULT_HOTSPOTS), True
    except Exception as error:
        print(f"Erro ao carregar hotspots do banco de dados: {error}")
        return DEFAULT_HOTSPOTS, False
