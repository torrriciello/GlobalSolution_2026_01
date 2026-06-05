#!/usr/bin/env python3
"""
Script de teste rápido — Adiciona hotspots de exemplo e lista.
Use para testar rapidamente o sistema.
"""

import subprocess
import sys

def run_command(cmd):
    print(f"\n{'='*60}")
    print(f"▶️  Executando: {' '.join(cmd)}")
    print(f"{'='*60}")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar comando: {e}")
        sys.exit(1)

def main():
    print("\n🔥 IgnisRoute — Script de Teste Rápido\n")
    
    # Inicializar banco
    print("📍 Etapa 1: Inicializando banco de dados...")
    run_command([sys.executable, "scripts/init_db.py"])
    
    # Adicionar hotspots de exemplo
    print("\n📍 Etapa 2: Adicionando hotspots de exemplo...")
    hotspots = [
        (-23.5934, -46.6305, "Foco em Vila Mariana", "Alto"),
        (-23.5473, -46.5498, "Fumaça em Tatuapé", "Médio"),
        (-23.5615, -46.7058, "Queimada em Pinheiros", "Alto"),
    ]
    
    for lat, lon, desc, severity in hotspots:
        run_command([sys.executable, "scripts/manage_hotspots.py", "add", 
                    str(lat), str(lon), desc, severity])
    
    # Listar hotspots
    print("\n📍 Etapa 3: Listando hotspots cadastrados...")
    run_command([sys.executable, "scripts/manage_hotspots.py", "list"])
    
    print("\n✅ Setup de teste concluído!")
    print("\n🚀 Próximo passo: Execute 'streamlit run app.py'\n")

if __name__ == "__main__":
    main()
