# Reponderação Amostral de Pesquisas Eleitorais (Datafolha)

Este projeto é uma ferramenta em Python desenvolvida para auditar e corrigir o viés amostral das pesquisas eleitorais presidenciais do Datafolha. 

O objetivo principal **não é prever o número exato da urna**, mas sim **apontar a direção correta da disputa** (quem realmente está na frente) e a margem de vantagem entre os candidatos, substituindo os pesos demográficos do instituto pelos dados reais da população brasileira (PNAD/IBGE).

## 🎯 O Problema que este Projeto Resolve

Institutos de pesquisa montam amostras que nem sempre representam a população real. Por exemplo, uma pesquisa pode entrevistar proporcionalmente mais pessoas de baixa renda do que existe de fato no país. Isso distorce o resultado final, fazendo com que o candidato forte nesse grupo pareça estar liderando com uma vantagem maior do que a real.

**A solução:** O motor pega a intenção de voto declarada em cada grupo (por Renda e Escolaridade) e aplica um **Fator de Correção** para equilibrar a balança.

## 🧮 A Matemática do Projeto (Passo a Passo)

O código não usa "chutes". Ele aplica pós-estratificação (post-stratification) com média ponderada, seguindo a matemática abaixo:

### 1. O Fator de Correção
Para cada grupo demográfico (ex: Renda até 2 SM, ou Ensino Superior), calculamos a diferença entre a população real e a amostra do instituto:

> **Fator = Peso PNAD (Real) / Peso Instituto (Amostra)**

### 2. O Cálculo do Voto (Média Ponderada)
O voto final de cada candidato é a soma dos votos de cada grupo multiplicados pelos seus fatores, dividida pela soma total dos fatores:

> **Voto = Σ (Voto no Grupo × Fator) / Σ Fator**

*Exemplo prático (Candidato X):*
* *Grupo A (Fator 0,5): 40% dos votos -> 40 × 0,5 = 20*
* *Grupo B (Fator 1,2): 30% dos votos -> 30 × 1,2 = 36*
* *Soma dos Votos: 20 + 36 = 56*
* *Soma dos Fatores: 0,5 + 1,2 = 1,7*
* *Voto Final: 56 / 1,7 = 32,94%*

### 3. A Média Final (Renda + Escolaridade)
O resultado da pesquisa é a média simples entre o cálculo feito na Renda e o cálculo feito na Escolaridade:

> **Final = (Resultado Renda + Resultado Escolaridade) / 2**

### 4. A Regra do 2º Turno (Votos Válidos)
Antes de aplicar os Fatores (Passos 1 e 2), o motor "limpa" os brancos e nulos, normalizando os votos do grupo para 100%:

> **Voto Normalizado = (Voto do Candidato / Soma dos Votos Válidos do Grupo) × 100**


## 📊 Resultados e Validação (Backtest)

A ferramenta foi testada com dados reais de diferentes eleições para provar sua eficácia em corrigir a direção do voto:

### 1º Turno (Votos Totais)
*   **2022 (Lula x Bolsonaro):** A pesquisa original mostrava uma vantagem exagerada de Lula. Após a reponderação, a diferença caiu para **Lula +3,22%**, aproximando-se muito mais da realidade da urna.
*   **2026 (Lula x Flávio):** As pesquisas originais apontavam Lula na frente. Após a correção pela PNAD, o cenário inverteu: **Flávio assumiu a liderança** (+1,31 e +2,39), captando a tendência real que as pesquisas não mostravam.

### 2º Turno (Votos Válidos)
*   **Outubro/2026:** O Datafolha divulgou empate técnico (50% a 50%). O nosso motor, ao rodar os dados corrigidos em votos válidos, apontou uma vantagem consistente de **Flávio +5,63 e +5,67 pontos**, demonstrando que a amostra original estava escondendo a força do candidato em determinados estratos.

## 🖥️ Saída do Código (Resultados Reais)

Abaixo está o output real gerado pelo script ao rodar as 5 bases de dados:

```text
===========================================================================
RESULTADOS DATAFOLHA — DATAFOLHA (22 a 23 de setembro de 2026) (VOTOS TOTAIS)
===========================================================================
RENDA          : Lula =  35.57% | Flavio =  40.19% | Diff =  -4.62
ESCOLARIDADE   : Lula =  38.67% | Flavio =  36.66% | Diff =  +2.01
---------------------------------------------------------------------------
FINAL Lula: 37.12%
FINAL Flavio: 38.43%
Diferença: -1.31 pontos

===========================================================================
RESULTADOS DATAFOLHA — DATAFOLHA (29 de setembro a 1 de outubro de 2026) (VOTOS TOTAIS)
===========================================================================
RENDA          : Lula =  40.62% | Flavio =  45.45% | Diff =  -4.82
ESCOLARIDADE   : Lula =  42.11% | Flavio =  42.07% | Diff =  +0.04
---------------------------------------------------------------------------
FINAL Lula: 41.36%
FINAL Flavio: 43.76%
Diferença: -2.39 pontos

===========================================================================
RESULTADOS DATAFOLHA — DATAFOLHA (30 de setembro e 1 de outubro de 2022) (VOTOS TOTAIS)
===========================================================================
RENDA          : Lula =  39.27% | Bolsonaro =  43.50% | Diff =  -4.23
ESCOLARIDADE   : Lula =  47.67% | Bolsonaro =  37.00% | Diff = +10.67
---------------------------------------------------------------------------
FINAL Lula: 43.47%
FINAL Bolsonaro: 40.25%
Diferença: +3.22 pontos

===========================================================================
RESULTADOS DATAFOLHA — DATAFOLHA (13 a 15 de outubro de 2026) (VOTOS VÁLIDOS)
===========================================================================
RENDA          : Lula =  45.25% | Flavio =  54.75% | Diff =  -9.51
ESCOLARIDADE   : Lula =  49.12% | Flavio =  50.88% | Diff =  -1.76
---------------------------------------------------------------------------
FINAL VÁLIDOS Lula: 47.18%
FINAL VÁLIDOS Flavio: 52.82%
Diferença: -5.63 pontos

===========================================================================
RESULTADOS DATAFOLHA — DATAFOLHA (20 a 22 de outubro de 2026) - PESQUISA DE HOJE (VOTOS VÁLIDOS)
===========================================================================
RENDA          : Lula =  45.46% | Flavio =  54.54% | Diff =  -9.08
ESCOLARIDADE   : Lula =  48.87% | Flavio =  51.13% | Diff =  -2.26
---------------------------------------------------------------------------
FINAL VÁLIDOS Lula: 47.16%
FINAL VÁLIDOS Flavio: 52.84%
Diferença: -5.67 pontos


## ⚖️ Comparação Final: Recálculo vs. Pesquisa Original vs. Urna

Aqui está a prova real da eficácia do motor. A tabela abaixo mostra a diferença entre o que o instituto publicou, o que o nosso código gerou após a reponderação, e o que a urna oficial (TSE) confirmou.

### 🔹 1º Turno (Votos Totais)

| Data da Pesquisa | 1. Resultado da Pesquisa (Datafolha) | 2. Nosso Recálculo (Reponderado PNAD) | 3. Resultado Oficial (Urna/TSE) |
| :--- | :--- | :--- | :--- |
| **30/09 e 01/10/2022** | Lula **50%** x Bolsonaro **36%**<br>*(Vantagem Lula +14)* | Lula **43,47%** x Bolsonaro **40,25%**<br>*(Lula +3,22)* | Lula **48,43%** x Bolsonaro **43,20%**<br>*(Lula +5,23)* |
| **22 e 23/09/2026** | Lula **40%** x Flávio **36%**<br>*(Vantagem Lula +4)* | Lula **37,12%** x Flávio **38,43%**<br>*(Flávio +1,31)* | Flávio **47,03%** x Lula **45,16%**<br>*(Flávio +1,87)* |
| **29/09 a 01/10/2026** | Lula **42%** x Flávio **38%**<br>*(Vantagem Lula +4)* | Lula **41,36%** x Flávio **43,76%**<br>*(Flávio +2,39)* | Flávio **47,03%** x Lula **45,16%**<br>*(Flávio +1,87)* |

**A Prova Matemática:** As pesquisas originais (Coluna 1) apontavam o Lula na frente em 2026. Quando aplicamos os pesos da PNAD (Coluna 2), a direção virou e o **Flávio apareceu na liderança**, captando exatamente a tendência que a urna oficial (Coluna 3) confirmou depois.

### 🔹 2º Turno (Votos Válidos)

| Data da Pesquisa | 1. Resultado da Pesquisa (Datafolha) | 2. Nosso Recálculo (Reponderado PNAD) | 3. Resultado Oficial (Urna/TSE) |
| :--- | :--- | :--- | :--- |
| **13 a 15/10/2026** | Flávio **51%** x Lula **49%**<br>*(Vantagem Flávio +2)* | Flávio **52,82%** x Lula **47,18%**<br>*(Flávio +5,63)* | *(Aguardando 2º turno)* |
| **20 a 22/10/2026** | Flávio **50%** x Lula **50%**<br>*(Empate Técnico)* | Flávio **52,84%** x Lula **47,16%**<br>*(Flávio +5,67)* | *(Aguardando 2º turno)* |

**A Prova Matemática:** O Datafolha divulgou um empate técnico (50% a 50%) na última pesquisa (Coluna 1). O nosso motor, ao corrigir o viés amostral (Coluna 2), apontou uma vantagem consistente de **Flávio (+5,6 pontos)**, mostrando que a amostra original ainda escondia a força do candidato em determinados estratos populacionais.
