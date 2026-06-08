CREATE OR REPLACE VIEW vw_focos_incendio AS
SELECT
    f.id_fato,
    rg.latitude,
    rg.longitude,

    fr.descricao_risco AS severity,

    CONCAT(
        m.nome_municipio,
        ' - ',
        e.uf
    ) AS description,

    ss.nome_sensor,

    f.distancia_risco_km,
    f.tempo_interdicao_minutos,
    f.raio_afetado_metros,

    dt.data_completa

FROM Fato_Ocorrencias_Incendio f

INNER JOIN Dim_Tempo dt
    ON dt.id_tempo = f.id_tempo

INNER JOIN Dim_Regiao_Geografica rg
    ON rg.id_regiao = f.id_regiao

INNER JOIN Dim_Municipio m
    ON m.id_municipio = rg.id_municipio

INNER JOIN Dim_Estado e
    ON e.id_estado = m.id_estado

INNER JOIN Dim_Ocorrencia_Fogo ofo
    ON ofo.id_ocorrencia_fogo = f.id_ocorrencia_fogo

INNER JOIN Dim_Faixa_Risco fr
    ON fr.id_faixa_risco = ofo.id_faixa_risco

INNER JOIN Dim_Sensor_Satelite ss
    ON ss.id_sensor_satelite = ofo.id_sensor_satelite;