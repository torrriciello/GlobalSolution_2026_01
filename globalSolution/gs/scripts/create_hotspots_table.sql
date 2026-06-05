-- Script SQL para criar a tabela de hotspots no PostgreSQL
-- Execute este script no seu banco de dados

CREATE TABLE IF NOT EXISTS hotspots (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    description VARCHAR(255),
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Criar índice para melhorar performance nas buscas espaciais
CREATE INDEX IF NOT EXISTS idx_hotspots_coordinates 
ON hotspots(latitude, longitude);

-- Inserir dados de exemplo (comentado - descomente se desejar)
-- INSERT INTO hotspots (latitude, longitude, description, severity) VALUES
-- (-23.5934, -46.6305, 'Foco de incêndio em Vila Mariana', 'Alto'),
-- (-23.5473, -46.5498, 'Fumaça intensa detectada em Tatuapé', 'Médio'),
-- (-23.5615, -46.7058, 'Queimada em Pinheiros', 'Alto');
