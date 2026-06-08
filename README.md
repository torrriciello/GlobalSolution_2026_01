# IgnisRoute SOC — Sistema de Inteligência Geoespacial

Sistema desenvolvido para a **Global Solution FIAP 2026**, voltado ao apoio de **Defesa Civil** e **Corpo de Bombeiros** na tomada de decisão durante incêndios florestais.

O IgnisRoute calcula rotas terrestres seguras para viaturas de emergência: extrai coordenadas de focos de calor ativos de um banco relacional, aplica a fórmula de **Haversine** para medir distâncias reais entre incêndios e o trajeto, detecta interseções com zonas de exclusão térmica e recalcula automaticamente um desvio seguro quando necessário.

A interface apresenta um **Centro de Operações Geoespaciais (SOC)** com indicadores táticos, contexto de missão, mapa interativo e exportação de relatórios.

---

## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Linguagem | Python 3.10+ |
| Interface | Streamlit + design system SOC customizado |
| Mapas | Folium + streamlit-folium |
| Banco de dados | PostgreSQL (`psycopg2`) com fallback Supabase |
| Configuração | python-dotenv |

---

## Funcionalidades

- Extração de focos de calor de banco relacional PostgreSQL (prioridade) ou Supabase REST
- Cálculo de distância geodésica com fórmula de Haversine
- Detecção de rota cruzando zona de exclusão térmica (raio configurável)
- Recálculo de desvio seguro com validação contra focos ativos
- Raio efetivo ponderado por severidade (Alto / Médio / Baixo)
- Saída estruturada em JSON (`output/analise_rota.json`)
- Exportação de mapa tático HTML (`output/rota_tatica.html`)
- Painel SOC com KPIs, recomendação tática e inteligência de ameaças
- Modo demonstração com dados locais quando o banco não está configurado

---

## Estrutura do Projeto

```text
ignisroute/
├── app.py                      # Ponto de entrada (Streamlit)
├── requirements.txt
├── .env.example
│
├── models/
│   └── route_result.py         # Resultado estruturado da análise
│
├── services/
│   ├── hotspot_repository.py   # Acesso unificado ao banco de dados
│   ├── route_orchestrator.py   # Orquestração da análise de rota
│   └── risk_service.py         # Avaliação de risco e desvio
│
├── maps/
│   └── map_service.py          # Mapa Folium com camadas táticas
│
├── utils/
│   └── haversine.py            # Trigonometria esférica
│
├── ui/
│   ├── layouts/
│   │   └── command_center.py   # Layout principal do SOC
│   ├── components/             # Header, KPIs, mapa, ameaças, exportação
│   ├── mission_context.py      # Contexto e decisão tática
│   ├── constants.py
│   └── styles.py
│
├── data/
│   └── hotspots.py             # Dados de demonstração (São Paulo)
│
├── database/
│   ├── schemas/                # DDL e views
│   └── docs/                   # Dicionário e modelagem
│
├── scripts/
│   ├── init_db.py              # Criação da tabela hotspots
│   └── manage_hotspots.py      # CRUD de focos via CLI
│
└── output/                     # Artefatos gerados (JSON, HTML)
```

---

## Instalação

### 1. Clonar e entrar no projeto

```bash
git clone <url-do-repositorio>
cd ignisroute
```

### 2. Ambiente virtual

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Dependências

```bash
pip install -r requirements.txt
```

---

## Configuração

Copie o arquivo de exemplo e preencha as credenciais:

```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```

### Variáveis de ambiente

| Variável | Prioridade | Descrição |
|----------|------------|-----------|
| `DB_URL` | 1 | URL de conexão PostgreSQL |

Exemplo:

```env
DB_URL=postgresql://usuario:senha@host:5432/banco
```

#### OBS: .env já está preenchido no arquivo zipado encaminhado para os professores.

---

## Execução

```bash
streamlit run app.py
```

Acesse em [http://localhost:8501](http://localhost:8501).

---

## Cenários operacionais

### Via Livre

Sem focos de calor na análise. A rota principal é validada diretamente.

### Alerta de Queimada

Focos ativos são carregados do banco (ou fallback local). O sistema:

1. Calcula a distância mínima de cada foco à rota (Haversine)
2. Verifica se algum foco está dentro do raio de tolerância
3. Interdita a rota original, se necessário
4. Calcula e valida um desvio seguro
5. Retorna status, contagem de focos, matriz de coordenadas e mapa

---

## Saída estruturada

Após cada análise, o sistema gera:

| Artefato | Caminho | Conteúdo |
|----------|---------|----------|
| Relatório JSON | `output/analise_rota.json` | Status, focos, rotas, parâmetros |
| Mapa HTML | `output/rota_tatica.html` | Mapa interativo standalone |

Campos principais do resultado:

```json
{
  "road_status": "LIVRE | INTERDITADA",
  "interfering_foci_count": 0,
  "monitored_foci_count": 3,
  "validated_route": [[-23.5048, -46.6299], "..."],
  "scenario": "Alerta de Queimada",
  "safety_radius_km": 5.0
}
```

---

## Fluxo de processamento

```text
Parâmetros (cenário + raio)
        │
        ▼
hotspot_repository ──► PostgreSQL → Supabase → fallback local
        │
        ▼
risk_service ──► Haversine + zona de exclusão térmica
        │
        ├── Rota livre ──► validated_route = rota original
        │
        └── Rota bloqueada ──► desvio validado ──► validated_route = desvio
        │
        ▼
Exportação JSON + HTML + painel SOC
```

---

## Região de operação

O cenário simulado utiliza coordenadas da **Região Metropolitana de São Paulo**.

---

## Autores

Projeto desenvolvido para a disciplina **Global Solution 2026 — FIAP**.

| Integrante | RM |
|------------|-----|
| Nicole Lourival | 561943 |
| Tiphany Nemet | 566355 |
| Isack Rafael | 561943 |
| Gabriel Torriciello | 564683 |
| Vinícius Mugnes | 563106 |

---

**IgnisRoute SOC v2.1** — Global Solution FIAP 2026
