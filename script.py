# ==============================================================================
# MOTOR DE CORREÇÃO ELEITORAL — DATAFOLHA
# Correção amostral baseada nos pesos populacionais da PNAD
# ==============================================================================

def rodar_bloco(votos_grupo, c1_nome, c2_nome, nome_bloco, pesos_inst, pesos_pnad):
    """Usado para o 1º Turno (Votos Totais)."""
    print("=" * 75)
    print(f"RESULTADOS DATAFOLHA — {nome_bloco} (VOTOS TOTAIS)")
    print("=" * 75)

    resultados = {}
    for var in ["renda", "escolaridade"]:
        soma_voto_1, soma_peso_1 = 0.0, 0.0
        soma_voto_2, soma_peso_2 = 0.0, 0.0

        for grupo in pesos_inst[var]:
            peso_correcao = pesos_pnad[var][grupo] / pesos_inst[var][grupo]
            v1 = votos_grupo[var][c1_nome][grupo]
            v2 = votos_grupo[var][c2_nome][grupo]

            soma_voto_1 += v1 * peso_correcao
            soma_peso_1 += peso_correcao
            soma_voto_2 += v2 * peso_correcao
            soma_peso_2 += peso_correcao

        res1 = soma_voto_1 / soma_peso_1
        res2 = soma_voto_2 / soma_peso_2
        resultados[var] = (res1, res2)
        print(f"{var.upper():<15}: {c1_nome} = {res1:6.2f}% | {c2_nome} = {res2:6.2f}% | Diff = {res1 - res2:+6.2f}")

    final_1 = sum(resultados[v][0] for v in resultados) / len(resultados)
    final_2 = sum(resultados[v][1] for v in resultados) / len(resultados)

    print("-" * 75)
    print(f"FINAL {c1_nome}: {final_1:.2f}%")
    print(f"FINAL {c2_nome}: {final_2:.2f}%")
    print(f"Diferença: {final_1 - final_2:+.2f} pontos\n")


def rodar_bloco_validos(votos_grupo, c1_nome, c2_nome, nome_bloco, pesos_inst, pesos_pnad):
    """Usado para o 2º Turno (Votos Válidos - normaliza para 100% e tira B/N)."""
    print("=" * 75)
    print(f"RESULTADOS DATAFOLHA — {nome_bloco} (VOTOS VÁLIDOS)")
    print("=" * 75)

    # Normaliza votos dentro de cada grupo para 100%
    votos_norm = {}
    for var in votos_grupo:
        votos_norm[var] = {c1_nome: {}, c2_nome: {}}
        for grupo in votos_grupo[var][c1_nome]:
            v1 = votos_grupo[var][c1_nome][grupo]
            v2 = votos_grupo[var][c2_nome][grupo]
            total = v1 + v2
            votos_norm[var][c1_nome][grupo] = (v1 / total) * 100
            votos_norm[var][c2_nome][grupo] = (v2 / total) * 100

    resultados = {}
    for var in ["renda", "escolaridade"]:
        soma_voto_1, soma_peso_1 = 0.0, 0.0
        soma_voto_2, soma_peso_2 = 0.0, 0.0

        for grupo in pesos_inst[var]:
            peso_correcao = pesos_pnad[var][grupo] / pesos_inst[var][grupo]
            v1 = votos_norm[var][c1_nome][grupo]
            v2 = votos_norm[var][c2_nome][grupo]

            soma_voto_1 += v1 * peso_correcao
            soma_peso_1 += peso_correcao
            soma_voto_2 += v2 * peso_correcao
            soma_peso_2 += peso_correcao

        res1 = soma_voto_1 / soma_peso_1
        res2 = soma_voto_2 / soma_peso_2
        resultados[var] = (res1, res2)
        print(f"{var.upper():<15}: {c1_nome} = {res1:6.2f}% | {c2_nome} = {res2:6.2f}% | Diff = {res1 - res2:+6.2f}")

    final_1 = sum(resultados[v][0] for v in resultados) / len(resultados)
    final_2 = sum(resultados[v][1] for v in resultados) / len(resultados)

    print("-" * 75)
    print(f"FINAL VÁLIDOS {c1_nome}: {final_1:.2f}%")
    print(f"FINAL VÁLIDOS {c2_nome}: {final_2:.2f}%")
    print(f"Diferença: {final_1 - final_2:+.2f} pontos\n")


# ==============================================================================
# PESOS DE REFERÊNCIA (PNAD)
# ==============================================================================

pesos_pnad = {
    "renda": {
        "ate_2_sm": 0.3519,
        "de_2_a_5_sm": 0.3926,
        "mais_de_5_sm": 0.2555,
    },
    "escolaridade": {
        "ate_medio": 0.81,
        "superior": 0.19,
    },
}


# ==============================================================================
# 1º TURNO (VOTOS TOTAIS)
# ==============================================================================

# BLOCO 1 — DATAFOLHA (22 a 23 de setembro de 2026)
pesos_inst_set2026 = {
    "renda": {"ate_2_sm": 0.50, "de_2_a_5_sm": 0.33, "mais_de_5_sm": 0.12},
    "escolaridade": {"ate_medio": 0.68, "superior": 0.32},
}
dados_set2026 = {
    "renda": {
        "Lula":   {"ate_2_sm": 46.0, "de_2_a_5_sm": 34.0, "mais_de_5_sm": 33.0},
        "Flavio": {"ate_2_sm": 32.0, "de_2_a_5_sm": 40.0, "mais_de_5_sm": 43.0},
    },
    "escolaridade": {
        "Lula":   {"ate_medio": 40.0, "superior": 36.0},
        "Flavio": {"ate_medio": 35.0, "superior": 40.0},
    },
}
rodar_bloco(dados_set2026, "Lula", "Flavio", "DATAFOLHA (22 a 23 de setembro de 2026)", pesos_inst_set2026, pesos_pnad)

# BLOCO 2 — DATAFOLHA (29 de setembro a 1 de outubro de 2026)
pesos_inst_out2026 = {
    "renda": {"ate_2_sm": 0.48, "de_2_a_5_sm": 0.34, "mais_de_5_sm": 0.14},
    "escolaridade": {"ate_medio": 0.75, "superior": 0.25},
}
dados_out2026 = {
    "renda": {
        "Lula":   {"ate_2_sm": 56.0, "de_2_a_5_sm": 35.0, "mais_de_5_sm": 38.0},
        "Flavio": {"ate_2_sm": 31.0, "de_2_a_5_sm": 49.0, "mais_de_5_sm": 49.0},
    },
    "escolaridade": {
        "Lula":   {"ate_medio": 45.0, "superior": 38.0},
        "Flavio": {"ate_medio": 40.0, "superior": 45.0},
    },
}
rodar_bloco(dados_out2026, "Lula", "Flavio", "DATAFOLHA (29 de setembro a 1 de outubro de 2026)", pesos_inst_out2026, pesos_pnad)

# BLOCO 3 — DATAFOLHA (30 de setembro e 1 de outubro de 2022)
pesos_inst_2022 = {
    "renda": {"ate_2_sm": 0.50, "de_2_a_5_sm": 0.33, "mais_de_5_sm": 0.12},
    "escolaridade": {"ate_medio": 0.68, "superior": 0.32},
}
dados_2022 = {
    "renda": {
        "Lula":      {"ate_2_sm": 57.0, "de_2_a_5_sm": 40.0, "mais_de_5_sm": 33.0},
        "Bolsonaro": {"ate_2_sm": 26.0, "de_2_a_5_sm": 44.0, "mais_de_5_sm": 49.0},
    },
    "escolaridade": {
        "Lula":      {"ate_medio": 49.0, "superior": 45.0},
        "Bolsonaro": {"ate_medio": 35.0, "superior": 41.0},
    },
}
rodar_bloco(dados_2022, "Lula", "Bolsonaro", "DATAFOLHA (30 de setembro e 1 de outubro de 2022)", pesos_inst_2022, pesos_pnad)


# ==============================================================================
# 2º TURNO (VOTOS VÁLIDOS)
# ==============================================================================

# BLOCO 4 — DATAFOLHA (13 a 15 de outubro de 2026)
pesos_inst_out2026_datafolha = {
    "renda": {"ate_2_sm": 0.49, "de_2_a_5_sm": 0.235, "mais_de_5_sm": 0.235},
    "escolaridade": {"ate_medio": 0.76, "superior": 0.24},
}
dados_out2026_datafolha = {
    "renda": {
        "Lula":   {"ate_2_sm": 53.0, "de_2_a_5_sm": 40.0, "mais_de_5_sm": 39.0},
        "Flavio": {"ate_2_sm": 38.0, "de_2_a_5_sm": 55.0, "mais_de_5_sm": 55.0},
    },
    "escolaridade": {
        "Lula":   {"ate_medio": 47.6, "superior": 40.0},
        "Flavio": {"ate_medio": 42.9, "superior": 50.0},
    },
}
rodar_bloco_validos(dados_out2026_datafolha, "Lula", "Flavio", "DATAFOLHA (13 a 15 de outubro de 2026)", pesos_inst_out2026_datafolha, pesos_pnad)


# BLOCO 5 — DATAFOLHA (20 a 22 de outubro de 2026) — PESQUISA DE HOJE
# RESULTADO OFICIAL: Flávio 47% | Lula 46% (Totais) / 50% x 50% (Válidos)
pesos_inst_out2026_nova = {
    "renda": {"ate_2_sm": 0.49, "de_2_a_5_sm": 0.235, "mais_de_5_sm": 0.235},
    "escolaridade": {"ate_medio": 0.76, "superior": 0.24},
}
dados_out2026_nova = {
    "renda": {
        "Lula":   {"ate_2_sm": 54.0, "de_2_a_5_sm": 39.0, "mais_de_5_sm": 40.0},
        "Flavio": {"ate_2_sm": 39.0, "de_2_a_5_sm": 54.0, "mais_de_5_sm": 54.0},
    },
    "escolaridade": {
        "Lula":   {"ate_medio": 51.0, "superior": 46.0},
        "Flavio": {"ate_medio": 49.0, "superior": 54.0},
    },
}
rodar_bloco_validos(dados_out2026_nova, "Lula", "Flavio", "DATAFOLHA (20 a 22 de outubro de 2026) - PESQUISA DE HOJE", pesos_inst_out2026_nova, pesos_pnad)
