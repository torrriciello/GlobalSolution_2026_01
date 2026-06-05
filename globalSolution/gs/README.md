# 🔥 IgnisRoute — Sistema Tático de Navegação

Sistema desenvolvido para a **Global Solution FIAP 2026**, com o objetivo de auxiliar órgãos como **Defesa Civil** e **Corpo de Bombeiros** na tomada de decisão durante ocorrências de incêndios florestais.

A aplicação monitora focos de incêndio, avalia riscos geográficos e determina automaticamente se uma rota operacional deve ser mantida ou desviada para garantir a segurança das equipes em campo.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Streamlit
- Folium
- Streamlit Folium
- Pandas
- python-dotenv
- psycopg2-binary

---

## 📦 Instalação

### 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd ignisroute
```

### 2. Criar ambiente virtual (opcional, mas recomendado)

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / MacOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração das Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para carregar a URL do banco de dados PostgreSQL.

### 1. Copie o arquivo de exemplo

#### Windows

```bash
copy .env.example .env
```

#### Linux / MacOS

```bash
cp .env.example .env
```

### 2. Preencha suas credenciais

Abra o arquivo `.env` criado e substitua os valores de exemplo pela URL de conexão do seu banco de dados PostgreSQL:

```env
DB_URL=postgresql://usuario:senha@host:porta/banco
```

---

## ▶️ Executando a Aplicação

Na raiz do projeto execute:

```bash
streamlit run app.py
```

Após a inicialização, o navegador abrirá automaticamente.

Caso não abra, acesse:

```text
http://localhost:8501
```

---

## 🧪 Cenários Disponíveis

### Cenário 1 — Via Livre

- Sem focos de incêndio ativos.
- A rota principal é mantida.
- Navegação direta até o destino.

### Cenário 2 — Alerta de Queimada

- Foco de incêndio detectado.
- O algoritmo calcula a distância entre a rota e o foco.
- Caso o incêndio esteja dentro da área de risco configurada, uma rota alternativa é ativada automaticamente.

---

## 🧠 Funcionalidades

- Visualização geográfica em mapa interativo.
- Monitoramento de focos de incêndio.
- Simulação de cenários operacionais.
- Cálculo de distância utilizando a fórmula de Haversine.
- Definição dinâmica do raio de segurança.
- Ativação automática de rotas de desvio.
- Painel de métricas em tempo real.

---

## � Cadastro de Hotspots (Focos de Incêndio)

### 1. Inicializar o Banco de Dados

Antes de usar a aplicação, crie a tabela `hotspots` no PostgreSQL:

#### Opção A — Executar script Python

```bash
python scripts/init_db.py
```

#### Opção B — Executar SQL manualmente

Abra sua ferramenta SQL (pgAdmin, DBeaver, etc.) e execute o arquivo:

```bash
scripts/create_hotspots_table.sql
```

### 2. Adicionar Hotspots

#### Opção A — Modo Interativo (Recomendado)

```bash
python scripts/manage_hotspots.py
```

Menu de opções:
- **1**: Adicionar novo hotspot (solicita latitude, longitude, descrição, severidade)
- **2**: Listar todos os hotspots cadastrados
- **3**: Remover um hotspot
- **4**: Sair

#### Opção B — Linha de Comando

```bash
# Adicionar hotspot
python scripts/manage_hotspots.py add -23.5934 -46.6305 "Foco em Vila Mariana" "Alto"

# Listar todos
python scripts/manage_hotspots.py list

# Remover hotspot
python scripts/manage_hotspots.py delete 1
```

#### Opção C — SQL Direto

```sql
INSERT INTO hotspots (latitude, longitude, description, severity) 
VALUES (-23.5934, -46.6305, 'Foco em Vila Mariana', 'Alto');
```

### 3. Campos da Tabela

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `id` | SERIAL | ID único (gerado automaticamente) |
| `latitude` | FLOAT | Coordenada de latitude |
| `longitude` | FLOAT | Coordenada de longitude |
| `description` | VARCHAR(255) | Descrição do hotspot |
| `severity` | VARCHAR(50) | Severidade: Alto, Médio, Baixo |
| `created_at` | TIMESTAMP | Data/hora de criação |

### 4. Usar na Aplicação

Ao executar `streamlit run app.py`, escolha o cenário **"Alerta de Queimada"** para ver os hotspots cadastrados sendo avaliados.

---

## 📌 Observações

- O projeto foi desenvolvido para fins acadêmicos.
- Possui mecanismo de fallback para funcionamento mesmo sem conexão com o banco de dados.
- As coordenadas utilizadas representam um cenário simulado baseado na região de **São Paulo capital e metropolitana**.
- Todos os hotspots cadastrados no PostgreSQL serão carregados automaticamente pela aplicação.

---

## 👨‍💻 Autores

Projeto desenvolvido para a disciplina **Global Solution 2026 - FIAP**.

Nicole Lourival - RM561943

Tiphany Nemet - RM566355

Isack Rafael - RM561943

Gabriel Torriciello - RM564683

Vinícius Mugnes - RM563106

---

**IgnisRoute MVP v1.0**
