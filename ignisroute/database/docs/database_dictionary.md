# Dicionário de Dados — IgnisRoute

## Visão Geral

O banco de dados do IgnisRoute utiliza modelagem Snowflake para armazenamento e análise de ocorrências de incêndios florestais.

O objetivo é permitir a correlação entre:

* Localização geográfica
* Dados temporais
* Severidade do evento
* Sensores responsáveis pela detecção
* Impacto operacional nas rotas

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

# Fato_Ocorrencias_Incendio

Tabela central do modelo analítico.

| Campo                    | Tipo    | Descrição                    |
| ------------------------ | ------- | ---------------------------- |
| id_fato                  | INT     | Identificador do evento      |
| id_tempo                 | INT     | Referência temporal          |
| id_regiao                | INT     | Referência geográfica        |
| id_ocorrencia_fogo       | INT     | Referência da ocorrência     |
| distancia_risco_km       | DECIMAL | Distância entre rota e foco  |
| tempo_interdicao_minutos | INT     | Tempo estimado de interdição |
| raio_afetado_metros      | DECIMAL | Área de impacto estimada     |
