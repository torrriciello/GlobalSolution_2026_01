# IgnisRoute SOC — Sistema de Inteligência Geoespacial

Sistema desenvolvido para a **Global Solution FIAP 2026**, voltado ao apoio de **Defesa Civil** e **Corpo de Bombeiros** na tomada de decisão durante incêndios florestais.

O IgnisRoute calcula rotas terrestres seguras para viaturas de emergência: extrai focos operacionais da view `vw_focos_ativos` (PostgreSQL/Supabase), aplica a fórmula de **Haversine** para medir distâncias reais entre incêndios e o trajeto, classifica o impacto com `status_ocorrencia` e `impacto_operacional`, detecta interseções com zonas de exclusão térmica e recalcula automaticamente um desvio seguro via **OSRM** quando necessário.

A interface apresenta um **Centro de Operações Geoespaciais (SOC)** com indicadores táticos, contexto de missão, mapa interativo e exportação de relatórios.

---

## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Linguagem | Python 3.10+ |
| Interface | Streamlit + design system SOC customizado |
| Mapas | Folium + streamlit-folium |
| Banco de dados | PostgreSQL (`psycopg2`) com fallback Supabase REST |
| Roteamento viário | OSRM — malha rodoviária real |
| Configuração | python-dotenv |

---

## Funcionalidades

- Extração de focos operacionais da view `vw_focos_ativos` (PostgreSQL ou Supabase REST)
- Classificação operacional por `status_ocorrencia` (ATIVO, MONITORADO, CONTROLADO, EXTINTO)
- Derivação de `impacto_operacional` (BLOQUEIO, DESVIO, MONITORAMENTO, CONTROLADO, EXTINTO)
- Cálculo de distância geodésica com fórmula de Haversine
- Bloqueio de rota apenas para focos **ATIVOS** dentro da zona de segurança
- Focos **MONITORADOS** exibidos no mapa sem interferir no trajeto
- Focos **CONTROLADOS** e **EXTINTOS** ignorados pela análise operacional
- Roteamento viário real via OSRM com desvio automático e validação de segurança
- Raio efetivo ponderado por severidade (Crítico / Alto / Médio / Baixo)
- Mapa tático com rota validada (verde), bloqueada (vermelha) e desvio (azul)
- Saída estruturada em JSON (`output/analise_rota.json`)
- Exportação de mapa tático HTML (`output/rota_tatica.html`)
- Painel SOC com KPIs, narrativa operacional e inteligência de ameaças

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
│   └── run_migration.py        # Migração SQL (status_ocorrencia) no Supabase
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
| `DB_URL` | 1 | URL de conexão PostgreSQL (Session Pooler Supabase) |
| `OSRM_URL` | — | Endpoint OSRM (padrão: `router.project-osrm.org`) |
| `OSRM_TIMEOUT` | — | Timeout da consulta OSRM em segundos (padrão: 12) |

Exemplo:

```env
DB_URL=postgresql://usuario:senha@host:5432/banco
OSRM_URL=https://router.project-osrm.org
OSRM_TIMEOUT=12
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

Sem focos de calor na análise. A rota principal é validada diretamente sobre a malha viária OSRM.

### Alerta de Queimada

Focos operacionais são carregados exclusivamente de `vw_focos_ativos`. O sistema:

1. Ignora focos com status CONTROLADO ou EXTINTO (já filtrados na view)
2. Exibe focos MONITORADOS no mapa sem bloquear o trajeto
3. Calcula a distância mínima de cada foco **ATIVO** à rota (Haversine)
4. Verifica se algum foco ATIVO está dentro do raio de segurança configurado
5. Interdita a rota original (vermelha) e desenha a zona de exclusão ao redor do foco
6. Busca desvio seguro via OSRM (rotas alternativas e waypoints viários)
7. Retorna status de missão, contagem de focos, matriz de coordenadas e mapa

#### Lógica por status de ocorrência

| `status_ocorrencia` | Efeito na navegação |
|---------------------|---------------------|
| ATIVO | Pode bloquear a rota se estiver na zona de segurança |
| MONITORADO | Visível no mapa; não interfere no trajeto |
| CONTROLADO | Ignorado pela análise |
| EXTINTO | Ignorado pela análise |

#### Cenários de demonstração (dados no Supabase)

| Cenário | Configuração | Resultado visual |
|---------|--------------|------------------|
| Rota livre | `id_fato = 1` → MONITORADO | Rota verde; foco em observação |
| Desvio automático | `id_fato = 2` → ATIVO (Alto) | Original vermelha, desvio azul, validada verde |
| Missão interrompida | `id_fato = 3, 4, 5` → ATIVO (Crítico) | Apenas rota bloqueada; status **MISSÃO INTERROMPIDA** |

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
  "monitored_foci_count": 1,
  "validated_route": [[-23.5048, -46.6299], "..."],
  "detour_found": true,
  "routing_source": "osrm",
  "scenario": "Alerta de Queimada",
  "safety_radius_km": 5.0
}
```

Cada foco carregado inclui `status_ocorrencia` e `impacto_operacional` para rastreabilidade operacional.

---

## Fluxo de processamento

```text
Parâmetros (cenário + raio + origem/destino)
        │
        ▼
route_builder ──► OSRM (rota viária real)
        │
        ▼
hotspot_repository ──► vw_focos_ativos (PostgreSQL → Supabase REST)
        │
        ▼
risk_service ──► Haversine + status_ocorrencia
        │
        ├── MONITORADO ──► exibe no mapa, não bloqueia
        ├── ATIVO fora da zona ──► sem interferência
        ├── ATIVO na zona + desvio OSRM ──► validated_route = desvio (verde)
        └── ATIVO na zona sem desvio ──► MISSÃO INTERROMPIDA (rota vermelha)
        │
        ▼
Exportação JSON + HTML + painel SOC
```

### Legenda do mapa tático

| Elemento | Cor | Significado |
|----------|-----|-------------|
| Rota validada | Verde (animada) | Trajeto aprovado para a missão |
| Rota original | Vermelha (tracejada) | Trecho bloqueado por foco ATIVO |
| Desvio viário | Azul | Alternativa calculada via OSRM |
| Zona de exclusão | Laranja | Área de risco ao redor do foco bloqueante |
| Foco crítico | Vermelho pulsante | ATIVO interferindo na rota |
| Foco monitorado | Âmbar pulsante | MONITORADO em observação |

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

**IgnisRoute SOC v2.2** — Global Solution FIAP 2026
