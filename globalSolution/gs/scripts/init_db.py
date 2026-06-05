#!/usr/bin/env python3
"""
Script para inicializar o banco de dados PostgreSQL com a tabela de hotspots.
Execute após configurar DB_URL/.env
"""

import os
import sys

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    return os.getenv("DB_URL") or os.getenv("DATABASE_URL")


def init_database():
    db_url = get_database_url()
    if not db_url:
        print("❌ Erro: DB_URL ou DATABASE_URL não configurado no .env")
        sys.exit(1)

    connect_kwargs = {
        "dsn": db_url,
    }

    if "supabase.com" in db_url:
        connect_kwargs["sslmode"] = "require"

    try:
        with psycopg2.connect(**connect_kwargs) as conn:
            with conn.cursor() as cursor:
                # Criar tabela se não existir
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS hotspots (
                        id SERIAL PRIMARY KEY,
                        latitude FLOAT NOT NULL,
                        longitude FLOAT NOT NULL,
                        description VARCHAR(255),
                        severity VARCHAR(50),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
                conn.commit()
                print("✅ Tabela 'hotspots' criada ou já existe.")

                # Verificar se há hotspots
                cursor.execute("SELECT COUNT(*) FROM hotspots;")
                count = cursor.fetchone()[0]
                print(f"📍 Total de hotspots no banco: {count}")

    except Exception as error:
        print(f"❌ Erro ao conectar ao banco: {error}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
