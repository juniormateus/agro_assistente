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

def densidade_semeadura(pms_gramas, populacao_desejada, germinacao_percentual):
    """
    calcula a densidade de semadura (kg/ha)

    Parâmetros:
    - PMS (Peso de mil semestes) em gramas
    - População desejada (plantas/ha)
    - Germinaçao esperada (Plantas/ha)
    """
    sementes_necessarias = populacao_desejada / (germinacao_percentual / 100)
    peso_total_gramas = (sementes_necessarias / 1000) * pms_gramas
    return peso_total_gramas / 1000 #Para retornas em kg/ha


def numero_linhas(area_ha, espac_linha, comprimento_linha):
    """
    Calcula o número de linhas de plantio em uma área específica.

    Parâmetros:
    - Área (ha)
    - Espaçamento entre linhas (m)
    - Comprimento de cada linha (m)

    Retorna:
    - Quantidade de linhas na área total
    """
    area_m2 = area_ha * 10000
    area_por_linha = espac_linha * comprimento_linha
    return area_m2 / area_por_linha


def comprimento_total_linhas(area_ha, espac_linha):
    """
    comprimento total de linhas em uma área

    Parâmetro:
    - Área (ha)
    - Espacamento entre linhas (m)
    """
    linhas_por_ha = 10000 / espac_linha
    return linhas_por_ha * area_ha

def estimativa_producao(populacao, produtividade_por_planta):
    """
    Estima a produção total por hectare (ou área especifica)
    
    Parâmetros:
    - População (plantas)
    - Produtividade por planta (kg/planta)
    """
    return populacao * produtividade_por_planta


