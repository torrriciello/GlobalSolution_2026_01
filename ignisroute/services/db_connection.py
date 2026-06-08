"""Utilitários de conexão com PostgreSQL / Supabase."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import unquote


def parse_database_url(database_url: str) -> dict[str, Any]:
    """
    Faz parse seguro da URL do banco, inclusive senhas com [, ], @ e outros caracteres.
    """
    url = database_url.strip()
    if "://" in url:
        url = url.split("://", 1)[1]

    if "@" not in url:
        raise ValueError("DATABASE_URL inválida: credenciais ausentes.")

    userinfo, remainder = url.rsplit("@", 1)
    user, _, password = userinfo.partition(":")
    if not user:
        raise ValueError("DATABASE_URL inválida: usuário ausente.")

    if "/" in remainder:
        host_port, dbname = remainder.split("/", 1)
        dbname = dbname.split("?", 1)[0] or "postgres"
    else:
        host_port, dbname = remainder, "postgres"

    if ":" in host_port:
        host, port_str = host_port.rsplit(":", 1)
        port = int(port_str)
    else:
        host, port = host_port, 5432

    return {
        "host": host,
        "port": port,
        "user": unquote(user),
        "password": unquote(password),
        "dbname": unquote(dbname),
    }


def extract_supabase_project_ref(host: str, user: str | None = None) -> str | None:
    """Extrai o project ref de hostnames ou usuário Supabase (postgres.<ref>)."""
    host = host.strip().lower()
    match = re.match(r"db\.([a-z0-9]+)\.supabase\.co$", host)
    if match:
        return match.group(1)

    if user:
        user_match = re.match(r"postgres\.([a-z0-9]+)$", user.strip().lower())
        if user_match:
            return user_match.group(1)

    pooler_match = re.match(r"aws-\d+-[a-z0-9-]+\.pooler\.supabase\.com$", host)
    if pooler_match and user:
        user_match = re.match(r"postgres\.([a-z0-9]+)$", user.strip().lower())
        if user_match:
            return user_match.group(1)

    return None


def build_supabase_rest_url(project_ref: str) -> str:
    return f"https://{project_ref}.supabase.co"


def connection_kwargs(database_url: str) -> dict[str, Any]:
    """Monta kwargs do psycopg2 a partir da URL."""
    params = parse_database_url(database_url)
    host = params["host"]

    connect_kwargs: dict[str, Any] = {
        **params,
        "connect_timeout": 10,
    }

    if "supabase.co" in host:
        connect_kwargs["sslmode"] = "require"

    return connect_kwargs


def friendly_connection_error(error: Exception, host: str | None = None) -> str:
    message = str(error).lower()

    if "could not translate host name" in message or "name or service not known" in message:
        if host and "supabase.co" in host:
            return (
                "Não foi possível alcançar o servidor PostgreSQL do Supabase. "
                "Redes sem IPv6 costumam falhar na conexão direta (db.*.supabase.co). "
                "Soluções: (1) adicione SUPABASE_URL e SUPABASE_KEY no .env para usar a API REST; "
                "(2) use a URL do Session Pooler no painel do Supabase (aws-0-*.pooler.supabase.com); "
                "(3) verifique se o projeto não está pausado."
            )
        return (
            "Não foi possível resolver o hostname do banco. "
            "Verifique DB_URL, conexão com a internet e se o projeto está ativo."
        )

    if "password authentication failed" in message:
        return "Autenticação recusada. Verifique usuário e senha no DB_URL."

    if "network is unreachable" in message:
        return (
            "Rede inacessível ao servidor do banco (comum em conexões IPv6). "
            "Configure SUPABASE_URL + SUPABASE_KEY ou use o Session Pooler do Supabase."
        )

    return f"Falha na conexão: {error}"
