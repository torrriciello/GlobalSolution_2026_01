/* ==========================================================
   DIM_STATUS_OCORRENCIA
========================================================== */

CREATE TABLE IF NOT EXISTS Dim_Status_Ocorrencia (
    id_status INT PRIMARY KEY,
    descricao_status VARCHAR(30) NOT NULL UNIQUE
);

INSERT INTO Dim_Status_Ocorrencia (
    id_status,
    descricao_status
)
VALUES
    (1, 'ATIVO'),
    (2, 'MONITORADO'),
    (3, 'CONTROLADO'),
    (4, 'EXTINTO')
ON CONFLICT (id_status)
DO NOTHING;


/* ==========================================================
   ALTERAÇÃO DA TABELA FATO
========================================================== */

ALTER TABLE Fato_Ocorrencias_Incendio
ADD COLUMN IF NOT EXISTS id_status INT;

ALTER TABLE Fato_Ocorrencias_Incendio
DROP CONSTRAINT IF EXISTS fk_fato_status;

ALTER TABLE Fato_Ocorrencias_Incendio
ADD CONSTRAINT fk_fato_status
FOREIGN KEY (id_status)
REFERENCES Dim_Status_Ocorrencia(id_status);


UPDATE Fato_Ocorrencias_Incendio
SET id_status = 1
WHERE id_status IS NULL;


CREATE OR REPLACE VIEW vw_focos_operacionais AS

SELECT

    f.id_fato,

    t.data_completa,

    m.nome_municipio,
    e.nome_estado,
    e.uf,

    b.nome_bioma,

    rg.latitude,
    rg.longitude,

    s.nome_sensor,

    fr.descricao_risco AS severity,

    st.descricao_status AS status_ocorrencia,

    f.distancia_risco_km,

    f.tempo_interdicao_minutos,

    f.raio_afetado_metros,

    CASE

        WHEN st.descricao_status = 'ATIVO'
             AND fr.descricao_risco = 'Crítico'
        THEN 'BLOQUEIO'

        WHEN st.descricao_status = 'ATIVO'
             AND fr.descricao_risco = 'Alto'
        THEN 'DESVIO'

        WHEN st.descricao_status = 'MONITORADO'
        THEN 'MONITORAMENTO'

        WHEN st.descricao_status = 'CONTROLADO'
        THEN 'CONTROLADO'

        WHEN st.descricao_status = 'EXTINTO'
        THEN 'EXTINTO'

        ELSE 'MONITORAMENTO'

    END AS impacto_operacional

FROM Fato_Ocorrencias_Incendio f

INNER JOIN Dim_Tempo t
    ON t.id_tempo = f.id_tempo

INNER JOIN Dim_Regiao_Geografica rg
    ON rg.id_regiao = f.id_regiao

INNER JOIN Dim_Municipio m
    ON m.id_municipio = rg.id_municipio

INNER JOIN Dim_Estado e
    ON e.id_estado = m.id_estado

INNER JOIN Dim_Bioma b
    ON b.id_bioma = m.id_bioma

INNER JOIN Dim_Ocorrencia_Fogo oc
    ON oc.id_ocorrencia_fogo = f.id_ocorrencia_fogo

INNER JOIN Dim_Faixa_Risco fr
    ON fr.id_faixa_risco = oc.id_faixa_risco

INNER JOIN Dim_Sensor_Satelite s
    ON s.id_sensor_satelite = oc.id_sensor_satelite

INNER JOIN Dim_Status_Ocorrencia st
    ON st.id_status = f.id_status;


CREATE OR REPLACE VIEW vw_focos_ativos AS

SELECT *
FROM vw_focos_operacionais

WHERE status_ocorrencia IN (
    'ATIVO',
    'MONITORADO'
);


CREATE OR REPLACE VIEW vw_dashboard_operacional AS

SELECT

    COUNT(*) FILTER (
        WHERE status_ocorrencia = 'ATIVO'
    ) AS focos_ativos,

    COUNT(*) FILTER (
        WHERE status_ocorrencia = 'MONITORADO'
    ) AS focos_monitorados,

    COUNT(*) FILTER (
        WHERE status_ocorrencia = 'CONTROLADO'
    ) AS focos_controlados,

    COUNT(*) FILTER (
        WHERE status_ocorrencia = 'EXTINTO'
    ) AS focos_extintos,

    COUNT(DISTINCT nome_sensor)
        AS sensores_operantes,

    ROUND(
        AVG(distancia_risco_km),
        2
    ) AS distancia_media_km,

    ROUND(
        AVG(tempo_interdicao_minutos),
        0
    ) AS tempo_medio_interdicao

FROM vw_focos_operacionais;


UPDATE Fato_Ocorrencias_Incendio
SET id_status = 2
WHERE id_fato = 1;


UPDATE Fato_Ocorrencias_Incendio
SET id_status = 1
WHERE id_fato = 2;


UPDATE Fato_Ocorrencias_Incendio
SET id_status = 1
WHERE id_fato IN (
    3,
    4,
    5
);
