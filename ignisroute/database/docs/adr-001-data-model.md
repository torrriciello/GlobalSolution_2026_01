# ADR-001 — Modelagem de Dados Snowflake

## Status

Aceito

---

## Contexto

O projeto IgnisRoute necessita armazenar informações relacionadas a:

* Ocorrências de incêndio
* Localização geográfica
* Dados temporais
* Classificação de risco
* Sensores de monitoramento

Além disso, o modelo deve permitir futuras expansões analíticas e integração com fontes externas.

---

## Decisão

Foi adotado o modelo dimensional Snowflake.

---

## Justificativa

O modelo Snowflake oferece:

* Maior normalização dos dados
* Redução de redundância
* Melhor governança de dados
* Facilidade para evolução futura
* Clareza conceitual para análises geoespaciais

---

## Consequências Positivas

* Estrutura organizada
* Facilidade de manutenção
* Integridade referencial
* Menor duplicação de informações
* Suporte a consultas analíticas

---

## Consequências Negativas

* Maior quantidade de JOINs
* Complexidade ligeiramente superior em comparação ao Star Schema

---

## Alternativas Avaliadas

### Star Schema

Vantagem:

* Consultas mais simples

Desvantagem:

* Maior redundância

### Banco Não Relacional

Vantagem:

* Flexibilidade

Desvantagem:

* Perda de integridade referencial

---

## Decisão Final

O modelo Snowflake foi escolhido por oferecer equilíbrio entre organização, escalabilidade e qualidade dos dados para o contexto do IgnisRoute.
