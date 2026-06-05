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
- Supabase

---

## 📦 Instalação

### 1. Clonar o projeto

```bash
git clone <url-do-repositorio>
cd ignisroute
```

### 2. Criar ambiente virtual (Opcional, mas recomendado)

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

O projeto utiliza variáveis de ambiente para armazenar credenciais sensíveis de acesso ao Supabase.

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

Abra o arquivo `.env` criado e substitua os valores de exemplo pelas credenciais do seu projeto Supabase:

```env
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-api
```

### 3. Instale as dependências

Certifique-se de que a biblioteca responsável pelo carregamento das variáveis de ambiente esteja instalada:

```bash
pip install python-dotenv
```

### Arquivo `.env.example`

O repositório disponibiliza um arquivo de exemplo:

```env
SUPABASE_URL=
SUPABASE_KEY=
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
- Integração com Supabase.
- Simulação de cenários operacionais.
- Cálculo de distância utilizando a Fórmula de Haversine.
- Definição dinâmica do raio de segurança.
- Ativação automática de rotas de desvio.
- Painel de métricas em tempo real.

---

## 📊 Estrutura Lógica

```text
Supabase
    │
    ▼
Carregamento de Focos
    │
    ▼
Algoritmo de Avaliação de Risco
    │
    ▼
Verificação de Interseção da Rota
    │
    ├── Livre
    │      ▼
    │   Rota Principal
    │
    └── Bloqueada
           ▼
      Rota de Desvio
           │
           ▼
     Exibição no Mapa
```

---

## 📌 Observações

- O projeto foi desenvolvido para fins acadêmicos.
- Possui mecanismo de fallback para funcionamento mesmo sem conexão com o banco de dados.
- As coordenadas utilizadas representam um cenário simulado baseado na região de Corumbá/MS.

---

## 👨‍💻 Autores

Projeto desenvolvido para a disciplina **Global Solution 2026 - FIAP**.

Nicole Lourival - RM561943​

Tiphany Nemet - RM566355​

Isack Rafael - RM561943​

Gabriel Torriciello - RM564683​

Vinícius Mugnes - RM563106​


--- 

**IgnisRoute MVP v1.0**
