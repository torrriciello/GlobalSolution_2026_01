# Projeto IgnisRoute

## Visão Geral

O IgnisRoute é um sistema de inteligência geoespacial desenvolvido para apoiar órgãos de emergência, Defesa Civil e Corpo de Bombeiros durante eventos de incêndio florestal.

O sistema identifica focos de calor, calcula zonas de risco e sugere rotas seguras para deslocamento operacional.

---

## Problema

Incêndios florestais podem:

* Interditar vias
* Aumentar o tempo de resposta
* Colocar equipes em risco
* Prejudicar operações de evacuação

Atualmente, a tomada de decisão depende de informações dispersas e atualizações manuais.

---

## Objetivo

Criar uma plataforma capaz de:

1. Monitorar focos de incêndio.
2. Calcular risco geográfico.
3. Identificar interferências em rotas.
4. Sugerir desvios automáticos.
5. Apoiar a tomada de decisão operacional.

---

## Arquitetura

### Frontend

* Streamlit

### Visualização Geográfica

* Folium
* Leaflet

### Backend

* Python

### Banco de Dados

* PostgreSQL
* Supabase

---

## Modelo de Dados

O banco utiliza arquitetura Snowflake.

Entidades principais:

* Tempo
* Região
* Bioma
* Município
* Estado
* Sensor Satelital
* Faixa de Risco
* Ocorrência de Fogo

Tabela Fato:

* Fato_Ocorrencias_Incendio

---

## Algoritmos

### Distância Geográfica

Fórmula de Haversine.

Objetivo:

Calcular distância real entre a rota operacional e os focos monitorados.

---

### Classificação de Risco

Baseada em:

* Distância do foco
* Severidade
* Raio operacional configurado

---

### Recalculo de Rotas

Fluxo:

Incêndio Detectado
→ Análise de Interferência
→ Zona de Exclusão
→ Bloqueio da Via
→ Geração de Desvio
→ Rota Validada

---

## Fonte de Dados

Os dados são consumidos da view:

vw_focos_incendio

A view consolida:

* Informações temporais
* Dados geográficos
* Sensores satelitais
* Severidade
* Indicadores operacionais

---

## Fluxo da Aplicação

Usuário seleciona cenário
→ Sistema consulta focos ativos
→ Distâncias são calculadas
→ Riscos são classificados
→ Rota é validada
→ Mapa tático é atualizado
→ Relatório JSON pode ser exportado

---

## Tecnologias

* Python 3.12+
* Streamlit
* Folium
* Supabase
* PostgreSQL
* psycopg2
* python-dotenv

---

## Contexto Acadêmico

Projeto desenvolvido para a Global Solution FIAP 2026.

Tema:

Prevenção, monitoramento e resposta a desastres naturais utilizando dados geoespaciais e inteligência analítica.
