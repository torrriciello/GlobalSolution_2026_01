# 📋 Como Cadastrar Focos de Incêndio no IgnisRoute

## Visão Geral do Sistema

O IgnisRoute agora usa um **PostgreSQL local/remoto** para armazenar hotspots (focos de incêndio). Aqui está como usar:

---

## 🔧 Opção 1: Inicialização Automática (Recomendado)

### Passo 1 — Instale as dependências:
```bash
pip install -r requirements.txt
```

### Passo 2 — Configure o `.env`:
```bash
# Windows
copy .env.example .env

# Linux/MacOS
cp .env.example .env
```

Edite `.env` e adicione a URL do seu PostgreSQL:
```env
DB_URL=postgresql://usuario:senha@host:5432/banco
```

### Passo 3 — Execute o script de teste rápido:
```bash
python scripts/quick_test.py
```

Isso fará tudo automaticamente:
- ✅ Inicializa o banco
- ✅ Cria a tabela `hotspots`
- ✅ Adiciona 3 hotspots de exemplo
- ✅ Lista os hotspots cadastrados

---

## 🔧 Opção 2: Processo Manual

### Etapa 1 — Criar o banco de dados:
```bash
python scripts/init_db.py
```

### Etapa 2 — Adicionar hotspots (modo interativo):
```bash
python scripts/manage_hotspots.py
```

Menu de opções:
```
1. Adicionar novo hotspot (pede latitude, longitude, descrição, severidade)
2. Listar hotspots cadastrados
3. Remover um hotspot
4. Sair
```

### Exemplo de entrada:
```
Latitude: -23.5934
Longitude: -46.6305
Descrição: Foco em Vila Mariana
Severidade: Alto
```

---

## 🔧 Opção 3: Linha de Comando

### Adicionar um hotspot:
```bash
python scripts/manage_hotspots.py add -23.5934 -46.6305 "Foco em Vila Mariana" "Alto"
```

### Listar todos:
```bash
python scripts/manage_hotspots.py list
```

### Remover um hotspot:
```bash
python scripts/manage_hotspots.py delete 1
```

---

## 🔧 Opção 4: SQL Direto (Avançado)

Se preferir usar uma ferramenta SQL (pgAdmin, DBeaver, etc.):

```sql
-- Criar tabela
CREATE TABLE IF NOT EXISTS hotspots (
    id SERIAL PRIMARY KEY,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    description VARCHAR(255),
    severity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserir hotspot
INSERT INTO hotspots (latitude, longitude, description, severity) 
VALUES (-23.5934, -46.6305, 'Foco em Vila Mariana', 'Alto');

-- Listar hotspots
SELECT * FROM hotspots ORDER BY created_at DESC;
```

---

## 📍 Coordenadas de Teste

Veja [HOTSPOTS_EXEMPLO.md](../HOTSPOTS_EXEMPLO.md) para uma lista completa de coordenadas prontas para usar na região de **São Paulo capital e metropolitana**.

**Exemplo rápido:**
```
Latitude:  -23.5934
Longitude: -46.6305
Descrição: Foco de incêndio em Vila Mariana
Severidade: Alto
```

---

## ▶️ Usar na Aplicação

Depois de adicionar hotspots:

```bash
streamlit run app.py
```

Selecione o cenário **"Alerta de Queimada"** no sidebar para ver os hotspots sendo avaliados.

---

## 📊 Estrutura da Tabela `hotspots`

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `id` | SERIAL | ID único (auto-incremento) |
| `latitude` | FLOAT | Coordenada Y |
| `longitude` | FLOAT | Coordenada X |
| `description` | VARCHAR(255) | Nome/descrição do foco |
| `severity` | VARCHAR(50) | Alto, Médio ou Baixo |
| `created_at` | TIMESTAMP | Data/hora de criação |

---

## ✅ Verificação

Para confirmar que está funcionando:

```bash
# 1. Inicializar
python scripts/init_db.py

# 2. Adicionar um hotspot
python scripts/manage_hotspots.py add -23.5934 -46.6305 "Foco em Vila Mariana" "Alto"

# 3. Listar
python scripts/manage_hotspots.py list
```

Se aparecer a tabela com o hotspot, está funcionando! ✅

---

## ❓ Troubleshooting

**Erro: "DB_URL ou DATABASE_URL não configurado"**
- Configure a variável no `.env` com a URL do PostgreSQL

**Erro: "connection refused"**
- Verifique se o PostgreSQL está rodando
- Confirme a URL está correta

**Erro: "table does not exist"**
- Execute `python scripts/init_db.py` para criar a tabela

---

## 🎯 Fluxo Recomendado

1. `pip install -r requirements.txt`
2. Editar `.env` com `DB_URL`
3. `python scripts/quick_test.py` (automático) **OU**
4. Manual: `init_db.py` → `manage_hotspots.py` → `streamlit run app.py`
5. Selecionar "Alerta de Queimada" no app
6. Ajustar raio de segurança para ver detecção

---

**Dúvidas? Veja também:**
- [GETTING_STARTED.md](../GETTING_STARTED.md) — Guia rápido
- [README.md](../README.md) — Documentação completa
- [HOTSPOTS_EXEMPLO.md](../HOTSPOTS_EXEMPLO.md) — Coordenadas de teste
