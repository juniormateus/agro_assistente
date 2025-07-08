def volume_calda(volume_por_hectare, area_tratada):
    """Calcula o volume total da calda (L)."""
    return volume_por_hectare * area_tratada


def dose_produto(dose_recomendada, area_tratada):
    """Calcula a dose total do produto (mL ou g)."""
    return dose_recomendada * area_tratada


def dose_tanque(dose_recomendada, volume_tanque, volume_aplicacao):
    """Calcula a dose total no tanque (mL ou g)."""
    return (dose_recomendada * volume_tanque) / volume_aplicacao


# --- Funções novas adicionadas ---

def diluicao_produto(volume_produto_concentrado, concentracao_desejada, volume_final_calda):
    """
    Calcula a quantidade de água necessária para diluir o produto.
    
    volume_produto_concentrado: volume do produto concentrado disponível (L)
    concentracao_desejada: concentração desejada na calda final (% ou fração decimal, ex: 0.1 para 10%)
    volume_final_calda: volume total de calda que deseja preparar (L)
    
    Retorna o volume de água necessário para diluir.
    """
    # volume de produto na calda final
    volume_produto_necessario = volume_final_calda * concentracao_desejada
    volume_agua_necessaria = volume_final_calda - volume_produto_necessario
    return max(volume_agua_necessaria, 0)


def numero_tanques(area_total, volume_por_hectare, volume_tanque):
    """
    Calcula o número de tanques necessários para aplicar na área.
    
    area_total: área total a ser tratada (ha)
    volume_por_hectare: volume de calda aplicado por hectare (L/ha)
    volume_tanque: volume de cada tanque (L)
    
    Retorna o número inteiro de tanques necessários (arredondado para cima).
    """
    from math import ceil
    volume_total = area_total * volume_por_hectare
    return ceil(volume_total / volume_tanque)


def tempo_aplicacao(area_total, velocidade_kmh, largura_m):
    """
    Estima o tempo de aplicação (em horas).
    
    area_total: área total a ser tratada (ha)
    velocidade_kmh: velocidade média do equipamento (km/h)
    largura_m: largura da barra de aplicação (metros)
    
    Retorna tempo estimado em horas.
    """
    # Convertendo largura para km (1 km = 1000 m)
    largura_km = largura_m / 1000
    # Área coberta por hora = velocidade * largura
    area_coberta_por_hora = velocidade_kmh * largura_km  # em km²/h
    # 1 km² = 100 ha
    area_coberta_ha_por_hora = area_coberta_por_hora * 100
    tempo_horas = area_total / area_coberta_ha_por_hora if area_coberta_ha_por_hora > 0 else 0
    return tempo_horas
