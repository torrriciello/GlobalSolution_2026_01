import os
from typing import Dict, List, Tuple

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

DEFAULT_HOTSPOTS = [
    {
        "id": 1,
        "latitude": -23.5934,
        "longitude": -46.6305,
        "severity": "Alto",
        "description": "Foco em Vila Mariana",
    },
    {
        "id": 2,
        "latitude": -23.5473,
        "longitude": -46.5498,
        "severity": "Médio",
        "description": "Fumaça em Tatuapé",
    },
    {
        "id": 3,
        "latitude": -23.5615,
        "longitude": -46.7058,
        "severity": "Baixo",
        "description": "Fogo em Pinheiros",
    },
]


def normalize_supabase_url(url: str) -> str:
    if not url:
        return url
    normalized = url.strip().rstrip("/")
    if normalized.endswith("/rest/v1"):
        normalized = normalized[: -len("/rest/v1")]
    return normalized


def load_env_vars() -> Tuple[str, str]:
    url = normalize_supabase_url(os.getenv("SUPABASE_URL", ""))
    key = os.getenv("SUPABASE_KEY", "")
    return url, key


def get_hotspots() -> Tuple[List[Dict], bool]:
    url, key = load_env_vars()
    if not url or not key:
        return DEFAULT_HOTSPOTS, False

    try:
        client = create_client(url, key)
        for table_name in ["focos", "incendios", "hotspots", "fire_hotspots"]:
            response = client.table(table_name).select("id,latitude,longitude,severity,description").limit(20).execute()
            data = getattr(response, "data", None)
            error = getattr(response, "error", None)
            if error:
                continue
            if data:
                return [
                    {
                        "id": item.get("id"),
                        "latitude": float(item.get("latitude")),
                        "longitude": float(item.get("longitude")),
                        "severity": item.get("severity", "Desconhecido"),
                        "description": item.get("description", "Foco de incêndio"),
                    }
                    for item in data
                    if item.get("latitude") is not None and item.get("longitude") is not None
                ], True
    except Exception:
        pass

    return DEFAULT_HOTSPOTS, False
