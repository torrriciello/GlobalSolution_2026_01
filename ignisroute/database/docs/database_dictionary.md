# Dicionário de Dados — IgnisRoute

## Visão Geral

O banco de dados do IgnisRoute utiliza modelagem Snowflake para armazenamento e análise de ocorrências de incêndios florestais.

O objetivo é permitir a correlação entre:

* Localização geográfica
* Dados temporais
* Severidade do evento
* Status operacional da ocorrência
* Sensores responsáveis pela detecção
* Impacto operacional nas rotas

---

## Views consumidas pela aplicação

| View | Uso |
|------|-----|
| `vw_focos_ativos` | Fonte principal do IgnisRoute — focos ATIVO e MONITORADO |
| `vw_focos_operacionais` | Visão analítica completa com todos os status |
| `vw_dashboard_operacional` | Agregações para painéis e indicadores |

---

# Dim_Ano

Armazena os anos utilizados na dimensão temporal.

| Campo  | Tipo | Descrição                  |
| ------ | ---- | -------------------------- |
| id_ano | INT  | Identificador único do ano |
| ano    | INT  | Ano calendário             |

---

# Dim_Mes

Armazena os meses do calendário.

| Campo      | Tipo        | Descrição               |
| ---------- | ----------- | ----------------------- |
| id_mes     | INT         | Identificador do mês    |
| numero_mes | INT         | Número do mês           |
| nome_mes   | VARCHAR(50) | Nome do mês             |
| id_ano     | INT         | Referência para Dim_Ano |

---

# Dim_Tempo

Representa datas específicas.

| Campo         | Tipo | Descrição               |
| ------------- | ---- | ----------------------- |
| id_tempo      | INT  | Identificador da data   |
| data_completa | DATE | Data completa           |
| id_mes        | INT  | Referência para Dim_Mes |

---

# Dim_Bioma

Armazena os biomas monitorados.

| Campo      | Tipo         | Descrição              |
| ---------- | ------------ | ---------------------- |
| id_bioma   | INT          | Identificador do bioma |
| nome_bioma | VARCHAR(100) | Nome do bioma          |

---

# Dim_Estado

Armazena os estados brasileiros.

| Campo       | Tipo         | Descrição                   |
| ----------- | ------------ | --------------------------- |
| id_estado   | INT          | Identificador do estado     |
| nome_estado | VARCHAR(100) | Nome do estado              |
| uf          | VARCHAR(2)   | Sigla da unidade federativa |

---

# Dim_Municipio

Representa municípios monitorados.

| Campo          | Tipo         | Descrição                  |
| -------------- | ------------ | -------------------------- |
| id_municipio   | INT          | Identificador do município |
| nome_municipio | VARCHAR(150) | Nome do município          |
| id_estado      | INT          | Referência para Dim_Estado |
| id_bioma       | INT          | Referência para Dim_Bioma  |

---

# Dim_Regiao_Geografica

Armazena coordenadas geográficas monitoradas.

| Campo        | Tipo    | Descrição                     |
| ------------ | ------- | ----------------------------- |
| id_regiao    | INT     | Identificador da região       |
| latitude     | DECIMAL | Latitude                      |
| longitude    | DECIMAL | Longitude                     |
| id_municipio | INT     | Referência para Dim_Municipio |

---

# Dim_Sensor_Satelite

Representa sensores utilizados para monitoramento.

| Campo              | Tipo        | Descrição               |
| ------------------ | ----------- | ----------------------- |
| id_sensor_satelite | INT         | Identificador do sensor |
| nome_sensor        | VARCHAR(50) | Nome do sensor          |

---

# Dim_Faixa_Risco

Classificação operacional do risco.

| Campo           | Tipo        | Descrição                     |
| --------------- | ----------- | ----------------------------- |
| id_faixa_risco  | INT         | Identificador da faixa        |
| descricao_risco | VARCHAR(50) | Baixo, Médio, Alto ou Crítico |

---

# Dim_Ocorrencia_Fogo

Relaciona sensores e classificação de risco.

| Campo              | Tipo | Descrição                           |
| ------------------ | ---- | ----------------------------------- |
| id_ocorrencia_fogo | INT  | Identificador da ocorrência         |
| id_faixa_risco     | INT  | Referência para Dim_Faixa_Risco     |
| id_sensor_satelite | INT  | Referência para Dim_Sensor_Satelite |

---

# Dim_Status_Ocorrencia

Classifica o estágio operacional de cada foco de incêndio.

| Campo             | Tipo        | Descrição                                      |
| ----------------- | ----------- | ---------------------------------------------- |
| id_status         | INT         | Identificador do status                        |
| descricao_status  | VARCHAR(30) | Descrição do status (única)                    |

### Domínio de valores

| id_status | descricao_status | Significado operacional                          |
| --------- | ---------------- | ------------------------------------------------ |
| 1         | ATIVO            | Foco ativo; pode bloquear rotas na zona de risco |
| 2         | MONITORADO       | Em observação; visível no mapa, sem bloqueio     |
| 3         | CONTROLADO       | Contido; ignorado pela análise de navegação      |
| 4         | EXTINTO          | Encerrado; ignorado pela análise de navegação   |

---

# Fato_Ocorrencias_Incendio

Tabela central do modelo analítico.

| Campo                    | Tipo    | Descrição                              |
| ------------------------ | ------- | -------------------------------------- |
| id_fato                  | INT     | Identificador do evento                |
| id_tempo                 | INT     | Referência temporal                    |
| id_regiao                | INT     | Referência geográfica                  |
| id_ocorrencia_fogo       | INT     | Referência da ocorrência               |
| id_status                | INT     | Referência para Dim_Status_Ocorrencia  |
| distancia_risco_km       | DECIMAL | Distância entre rota e foco            |
| tempo_interdicao_minutos | INT     | Tempo estimado de interdição           |
| raio_afetado_metros      | DECIMAL | Área de impacto estimada               |

---

# vw_focos_operacionais

View analítica que consolida todas as dimensões e deriva o impacto operacional.

| Campo                  | Tipo    | Origem / Descrição                                              |
| ---------------------- | ------- | --------------------------------------------------------------- |
| id_fato                | INT     | Identificador do evento                                         |
| data_completa          | DATE    | Data da detecção                                                |
| nome_municipio         | VARCHAR | Município do foco                                               |
| nome_estado            | VARCHAR | Estado                                                          |
| uf                     | VARCHAR | Sigla da UF                                                     |
| nome_bioma             | VARCHAR | Bioma associado                                                 |
| latitude               | DECIMAL | Coordenada geográfica                                           |
| longitude              | DECIMAL | Coordenada geográfica                                           |
| nome_sensor            | VARCHAR | Sensor satelital de detecção                                    |
| severity               | VARCHAR | Faixa de risco: Baixo, Médio, Alto ou Crítico                   |
| status_ocorrencia      | VARCHAR | Status da ocorrência (ATIVO, MONITORADO, CONTROLADO, EXTINTO)   |
| distancia_risco_km     | DECIMAL | Distância de referência rota–foco                               |
| tempo_interdicao_minutos | INT   | Tempo estimado de interdição                                    |
| raio_afetado_metros    | DECIMAL | Raio de impacto em metros                                       |
| impacto_operacional    | VARCHAR | Classificação derivada para navegação (ver regra abaixo)        |

### Regra de `impacto_operacional`

| Condição                                      | impacto_operacional |
| --------------------------------------------- | ------------------- |
| ATIVO + severidade Crítico                    | BLOQUEIO            |
| ATIVO + severidade Alto                       | DESVIO              |
| MONITORADO                                    | MONITORAMENTO       |
| CONTROLADO                                    | CONTROLADO          |
| EXTINTO                                       | EXTINTO             |
| Demais combinações                            | MONITORAMENTO       |

---

# vw_focos_ativos

View consumida pelo IgnisRoute. Retorna apenas focos com status operacional relevante.

```sql
SELECT * FROM vw_focos_operacionais
WHERE status_ocorrencia IN ('ATIVO', 'MONITORADO');
```

Focos CONTROLADO e EXTINTO são excluídos desta view e não participam da análise de rota.

---

# vw_dashboard_operacional

View de agregação para indicadores do painel SOC.

| Campo                    | Tipo    | Descrição                                    |
| ------------------------ | ------- | -------------------------------------------- |
| focos_ativos             | BIGINT  | Contagem de focos com status ATIVO           |
| focos_monitorados        | BIGINT  | Contagem de focos com status MONITORADO      |
| focos_controlados        | BIGINT  | Contagem de focos com status CONTROLADO      |
| focos_extintos           | BIGINT  | Contagem de focos com status EXTINTO         |
| sensores_operantes       | BIGINT  | Quantidade distinta de sensores com registro |
| distancia_media_km       | NUMERIC | Média de `distancia_risco_km`                |
| tempo_medio_interdicao   | NUMERIC | Média de `tempo_interdicao_minutos`          |

---

## Cenários de demonstração

Os registros abaixo configuram os três modos visuais do mapa tático:

| id_fato   | id_status | status_ocorrencia | Cenário esperado        |
| --------- | --------- | ----------------- | ----------------------- |
| 1         | 2         | MONITORADO        | Rota livre              |
| 2         | 1         | ATIVO             | Desvio automático       |
| 3, 4, 5   | 1         | ATIVO             | Missão interrompida     |

Script de migração: `database/schemas/03_status_ocorrencia.sql` (executável via `scripts/run_migration.py`).
