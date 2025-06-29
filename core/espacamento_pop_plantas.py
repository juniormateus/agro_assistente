def populacao_plantas(espac_entre_linhas, espac_entre_plantas):
    """
    Calcula a população de plantas por hectare

    Parâmentros:
    - Espaçamento entre linhas(m)
    - Espaçamento entre plantas (m)
    """
    return (10000) / (espac_entre_linhas * espac_entre_plantas)


def numero_plantas_area(populacao_plantas, area):
    """
    Calcula o Número total de plantas para uma área específica

    Parâmetros:
    - População (Plantas/ha)
    - Área (ha)
    """
    return populacao_plantas * area


def espacamento_plantas_populacao_desejada(pop_desejada, espac_entre_linhas2):
    """
    Espaçamento entre plantas usar para atingir uma população alvo (mantendo o espaçamento entre linhas fixo)
    
    Parâmetros:
    - População desejada (plantas/ha)
    - Espaçamento entre linhas (m)
    """
    return (10000) / (pop_desejada * espac_entre_linhas2)
