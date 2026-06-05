-- Criação das Tabelas de Dimensão (Hierarquia: Menor dependência para maior dependência)

-- 1. Dimensão Tempo
CREATE TABLE Dim_Ano (
    id_ano INT PRIMARY KEY,
    ano INT NOT NULL
);

CREATE TABLE Dim_Mes (
    id_mes INT PRIMARY KEY,
    numero_mes INT NOT NULL,
    nome_mes VARCHAR(50) NOT NULL,
    id_ano INT REFERENCES Dim_Ano(id_ano)
);

CREATE TABLE Dim_Tempo (
    id_tempo INT PRIMARY KEY,
    data_completa DATE NOT NULL,
    id_mes INT REFERENCES Dim_Mes(id_mes)
);

-- 2. Dimensão Região
CREATE TABLE Dim_Bioma (
    id_bioma INT PRIMARY KEY,
    nome_bioma VARCHAR(100) NOT NULL
);

CREATE TABLE Dim_Estado (
    id_estado INT PRIMARY KEY,
    nome_estado VARCHAR(100) NOT NULL,
    uf VARCHAR(2) NOT NULL
);

CREATE TABLE Dim_Municipio (
    id_municipio INT PRIMARY KEY,
    nome_municipio VARCHAR(150) NOT NULL,
    id_estado INT REFERENCES Dim_Estado(id_estado),
    id_bioma INT REFERENCES Dim_Bioma(id_bioma)
);

CREATE TABLE Dim_Regiao_Geografica (
    id_regiao INT PRIMARY KEY,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    id_municipio INT REFERENCES Dim_Municipio(id_municipio)
);

-- 3. Dimensão Severidade
CREATE TABLE Dim_Sensor_Satelite (
    id_sensor_satelite INT PRIMARY KEY,
    nome_sensor VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Faixa_Risco (
    id_faixa_risco INT PRIMARY KEY,
    descricao_risco VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Ocorrencia_Fogo (
    id_ocorrencia_fogo INT PRIMARY KEY,
    id_faixa_risco INT REFERENCES Dim_Faixa_Risco(id_faixa_risco),
    id_sensor_satelite INT REFERENCES Dim_Sensor_Satelite(id_sensor_satelite)
);

-- 4. Tabela Fato
CREATE TABLE Fato_Ocorrencias_Incendio (
    id_fato INT PRIMARY KEY,
    id_tempo INT REFERENCES Dim_Tempo(id_tempo),
    id_regiao INT REFERENCES Dim_Regiao_Geografica(id_regiao),
    id_ocorrencia_fogo INT REFERENCES Dim_Ocorrencia_Fogo(id_ocorrencia_fogo),
    distancia_risco_km DECIMAL(10, 2),
    tempo_interdicao_minutos INT,
    raio_afetado_metros DECIMAL(10, 2)
);
