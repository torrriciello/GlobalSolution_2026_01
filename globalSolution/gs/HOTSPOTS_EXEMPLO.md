# 📍 Exemplos de Coordenadas para Hotspots

Use estas coordenadas de exemplo para testar o IgnisRoute. Todas referem-se à região de São Paulo capital e metropolitana.

## Hotspots de Exemplo

### 1. Foco em Vila Mariana (Alto Risco)
```
Latitude:  -23.5934
Longitude: -46.6305
Descrição: Foco de incêndio próximo à avenida
Severidade: Alto
```

**Para adicionar:**
```bash
python scripts/manage_hotspots.py add -23.5934 -46.6305 "Foco em Vila Mariana" "Alto"
```

---

### 2. Fumaça em Tatuapé (Risco Médio)
```
Latitude:  -23.5473
Longitude: -46.5498
Descrição: Fumaça intensa detectada na zona leste
Severidade: Médio
```

**Para adicionar:**
```bash
python scripts/manage_hotspots.py add -23.5473 -46.5498 "Fumaça em Tatuapé" "Médio"
```

---

### 3. Queimada em Pinheiros (Alto Risco)
```
Latitude:  -23.5615
Longitude: -46.7058
Descrição: Fogo em área residencial da zona oeste
Severidade: Alto
```

**Para adicionar:**
```bash
python scripts/manage_hotspots.py add -23.5615 -46.7058 "Queimada em Pinheiros" "Alto"
```

---

### 4. Fogo na Avenida Paulista (Risco Médio)
```
Latitude:  -23.5615
Longitude: -46.6560
Descrição: Fogo controlado em obra na região central
Severidade: Médio
```

**Para adicionar:**
```bash
python scripts/manage_hotspots.py add -23.5615 -46.6560 "Fogo Avenida Paulista" "Médio"
```

---

### 5. Foco na zona leste (Risco Baixo)
```
Latitude:  -23.5600
Longitude: -46.5300
Descrição: Fogo residual em terreno baldio
Severidade: Baixo
```

**Para adicionar:**
```bash
python scripts/manage_hotspots.py add -23.5600 -46.5300 "Foco zona leste" "Baixo"
```

---

## Rota Principal de Teste

A rota principal utilizada na simulação passa por São Paulo:

```
Ponto 1: -23.5048, -46.6299  (Saída - Santana, zona norte)
Ponto 2: -23.5505, -46.6333  (Intermediário - Centro)
Ponto 3: -23.5934, -46.6305  (Destino - Vila Mariana, zona sul)
```

## 🧪 Teste Rápido

1. **Inicialize o banco:**
   ```bash
   python scripts/init_db.py
   ```

2. **Adicione alguns hotspots:**
   ```bash
   python scripts/manage_hotspots.py
   # (escolha opção 1 e adicione manualmente, ou use os comandos acima)
   ```

3. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

4. **Selecione "Alerta de Queimada"** no sidebar para ver os hotspots sendo avaliados.

5. **Ajuste o raio de segurança** para ver a detecção de rotas bloqueadas.

---

## 📝 Notas

- As coordenadas de latitude/longitude devem estar no intervalo [-90, 90] e [-180, 180] respectivamente.
- A severidade pode ser: **Alto**, **Médio**, **Baixo**.
- Você pode adicionar quantos hotspots desejar.
- Use coordenadas do mundo real para simular cenários reais.

---
