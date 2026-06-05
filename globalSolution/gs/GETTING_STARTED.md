# 🚀 Guia Rápido de Início

## 1️⃣ Configuração Inicial (5 minutos)

### Instale as dependências:
```bash
cd gs
pip install -r requirements.txt
```

### Configure o banco de dados no `.env`:
```bash
copy .env.example .env
```

Edite `.env` e adicione sua URL do PostgreSQL:
```env
DB_URL=postgresql://usuario:senha@localhost:5432/ignisroute
```

## 2️⃣ Inicialize o Banco de Dados

```bash
python scripts/init_db.py
```

Isso criará a tabela `hotspots` automaticamente.

## 3️⃣ Adicione Hotspots (Focos de Incêndio)

### Modo interativo (recomendado para iniciantes):
```bash
python scripts/manage_hotspots.py
```

### Ou adicione via linha de comando:
```bash
python scripts/manage_hotspots.py add -23.5934 -46.6305 "Foco em Vila Mariana" "Alto"
python scripts/manage_hotspots.py list
```

👉 **Veja [HOTSPOTS_EXEMPLO.md](HOTSPOTS_EXEMPLO.md) para coordenadas de teste.**

## 4️⃣ Execute a Aplicação

```bash
streamlit run app.py
```

O navegador abrirá automaticamente em: `http://localhost:8501`

## 5️⃣ Teste os Cenários

1. **Via Livre**: Sem hotspots ativados
2. **Alerta de Queimada**: Com hotspots para avaliação de risco

---

## 🎯 Seu Fluxo de Trabalho

```
┌─────────────────────────────┐
│  1. Configurar .env         │
│     (DB_URL)                │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  2. Criar Tabelas           │
│     (init_db.py)            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  3. Adicionar Hotspots      │
│     (manage_hotspots.py)    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│  4. Rodar App Streamlit     │
│     (streamlit run app.py)  │
└─────────────────────────────┘
```

---

## ❓ Perguntas Frequentes

**P: Não tenho um PostgreSQL local. E agora?**  
R: Use um PostgreSQL remoto (ex: Supabase, Railway, etc.) e configure a URL em `.env`.

**P: Onde vejo os hotspots cadastrados?**  
R: Execute `python scripts/manage_hotspots.py list` ou use ferramentas como pgAdmin.

**P: Como testar sem banco de dados?**  
R: A aplicação usa dados de fallback automaticamente se `DB_URL` não estiver configurado.

**P: Quais são as coordenadas da rota principal?**  
R: 
- Saída: `-23.5048, -46.6299` (Santana, zona norte)
- Intermediário: `-23.5505, -46.6333` (Centro)
- Destino: `-23.5934, -46.6305` (Vila Mariana, zona sul)

---

## 📚 Próximos Passos

- Leia [README.md](README.md) para detalhes técnicos completos
- Consulte [HOTSPOTS_EXEMPLO.md](HOTSPOTS_EXEMPLO.md) para exemplos de coordenadas
- Explore o código-fonte em `app.py`, `maps/`, `services/`, `data/`

---

**Pronto! Você está no comando do IgnisRoute! 🔥🗺️**
