#!/usr/bin/env python3
"""
Script para inserir/gerenciar hotspots no banco PostgreSQL.
Use para adicionar focos de incêndio manualmente.
"""

import os
import sys

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_database_url():
    return os.getenv("DB_URL") or os.getenv("DATABASE_URL")


def add_hotspot(latitude: float, longitude: float, description: str, severity: str) -> bool:
    db_url = get_database_url()
    if not db_url:
        print("❌ Erro: DB_URL ou DATABASE_URL não configurado no .env")
        return False

    connect_kwargs = {
        "dsn": db_url,
    }

    if "supabase.com" in db_url:
        connect_kwargs["sslmode"] = "require"

    try:
        with psycopg2.connect(**connect_kwargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO hotspots (latitude, longitude, description, severity) VALUES (%s, %s, %s, %s)",
                    (latitude, longitude, description, severity),
                )
                conn.commit()
                print(f"✅ Hotspot adicionado: ({latitude}, {longitude}) - {description}")
                return True
    except Exception as error:
        print(f"❌ Erro ao adicionar hotspot: {error}")
        return False


def list_hotspots():
    db_url = get_database_url()
    if not db_url:
        print("❌ Erro: DB_URL ou DATABASE_URL não configurado no .env")
        return

    connect_kwargs = {
        "dsn": db_url,
    }

    if "supabase.com" in db_url:
        connect_kwargs["sslmode"] = "require"

    try:
        with psycopg2.connect(**connect_kwargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT id, latitude, longitude, description, severity, created_at FROM hotspots ORDER BY created_at DESC;")
                rows = cursor.fetchall()
                
                if not rows:
                    print("❌ Nenhum hotspot cadastrado.")
                    return
                
                print("\n📍 Hotspots cadastrados:\n")
                print(f"{'ID':<5} {'Latitude':<12} {'Longitude':<12} {'Descrição':<30} {'Severidade':<10}")
                print("-" * 80)
                for row in rows:
                    print(f"{row[0]:<5} {row[1]:<12.4f} {row[2]:<12.4f} {row[3]:<30} {row[4]:<10}")
                print()

    except Exception as error:
        print(f"❌ Erro ao listar hotspots: {error}")


def delete_hotspot(hotspot_id: int) -> bool:
    db_url = get_database_url()
    if not db_url:
        print("❌ Erro: DB_URL ou DATABASE_URL não configurado no .env")
        return False

    connect_kwargs = {
        "dsn": db_url,
    }

    if "supabase.com" in db_url:
        connect_kwargs["sslmode"] = "require"

    try:
        with psycopg2.connect(**connect_kwargs) as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM hotspots WHERE id = %s;", (hotspot_id,))
                conn.commit()
                print(f"✅ Hotspot {hotspot_id} removido.")
                return True
    except Exception as error:
        print(f"❌ Erro ao remover hotspot: {error}")
        return False


def interactive_menu():
    while True:
        print("\n🔥 IgnisRoute — Gerenciador de Hotspots")
        print("=" * 50)
        print("1. Adicionar novo hotspot")
        print("2. Listar hotspots")
        print("3. Remover hotspot")
        print("4. Sair")
        print("=" * 50)
        
        choice = input("Escolha uma opção (1-4): ").strip()
        
        if choice == "1":
            try:
                lat = float(input("Latitude: "))
                lon = float(input("Longitude: "))
                desc = input("Descrição: ")
                severity = input("Severidade (Alto/Médio/Baixo): ")
                add_hotspot(lat, lon, desc, severity)
            except ValueError:
                print("❌ Entrada inválida. Use números para latitude/longitude.")
        
        elif choice == "2":
            list_hotspots()
        
        elif choice == "3":
            try:
                hotspot_id = int(input("ID do hotspot a remover: "))
                delete_hotspot(hotspot_id)
            except ValueError:
                print("❌ ID inválido.")
        
        elif choice == "4":
            print("Até logo! 👋")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Modo linha de comando
        if sys.argv[1] == "list":
            list_hotspots()
        elif sys.argv[1] == "add" and len(sys.argv) >= 6:
            add_hotspot(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5])
        elif sys.argv[1] == "delete" and len(sys.argv) >= 3:
            delete_hotspot(int(sys.argv[2]))
        else:
            print("Uso:")
            print("  python manage_hotspots.py list")
            print("  python manage_hotspots.py add <lat> <lon> <descricao> <severidade>")
            print("  python manage_hotspots.py delete <id>")
            print("  python manage_hotspots.py (modo interativo)")
    else:
        # Modo interativo
        interactive_menu()
